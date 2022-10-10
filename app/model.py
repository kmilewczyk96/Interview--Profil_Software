import asyncio
import csv
import json
from urllib.parse import urljoin

import httpx
import typer
import validators
from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup
from httpx import AsyncClient

from app import ERRORS, CONNECTION_ERROR
from app.page_details import PageDetails
from app.command_validators import CommandValidators
from app.utils import count_time_execution


class Model:
    """Contains methods which execute App's CLI commands."""
    def __init__(self, requests_limiter=30):
        """:param requests_limiter: Optional parameter that limits frequency of requests send to the page."""
        self.throttler = AsyncLimiter(max_rate=requests_limiter, time_period=1)
        self.page_details = PageDetails()
        self.validator = CommandValidators()

    @count_time_execution
    def crawl(self, url: str, extension: str, path: str):
        """Crawls the page and its subpages. Exports data to provided output in one of two available extensions."""
        self.page_details.create_record(url=url, is_base=True)
        self._collect_data(urls=[url])
        output = f'{path}.{extension}'
        if extension.lower() == 'csv':
            self._save_as_csv(output=output)
        if extension.lower() == 'json':
            self._save_as_json(output=output)

    @count_time_execution
    def print_tree(self, url: str) -> list:
        """
        Crawls the page and its subpages.
        Returns list of dicts, which contain: URLs, their indentation and subpages count.
        """
        self.page_details.create_record(url=url, is_base=True)
        self._collect_data(urls=[url])
        urls = [url for url in self.page_details.data]
        # Sort urls by the indentation:
        urls.sort(key=lambda x: x.count('/'))

        excluded = []
        tree = []

        def _search_for_children(current_url, indentation=0):
            subpages_count = 0
            if current_url.endswith('/'):
                for u in urls:
                    if u.startswith(current_url) and u not in excluded:
                        excluded.append(u)
                        subpages_count += _search_for_children(u, indentation + 1) + 1

            tree.append({'url': current_url, 'indentation': indentation, 'subpages_count': subpages_count})
            return subpages_count

        # Create tree:
        excluded.append(url)
        _search_for_children(url)
        tree.reverse()

        return tree

    async def _get_requests(self, url: str, client: AsyncClient) -> list:
        """Sends request to the URL. Returns new links from requested page."""
        # You can change throttling value by setting model's requests_limit parameter.
        async with self.throttler:
            try:
                typer.echo(f'Sending request to: {url}')
                request = await client.get(url=url, follow_redirects=False)
            except TimeoutError:
                typer.secho(f'Request timeout for: {url}', fg=typer.colors.YELLOW)
                return []
            except httpx.ConnectError:
                typer.secho(ERRORS[CONNECTION_ERROR], fg=typer.colors.RED)
                raise typer.Exit()
            else:
                return self._search_for_links(url=url, request=request)

    async def _run(self, urls: list) -> tuple:
        """Coordinates collecting requests. Returns tuple of new URLs to crawl."""
        async with AsyncClient(timeout=120, verify=False) as client:
            urls_to_crawl = []
            for url in urls:
                urls_to_crawl.append(self._get_requests(url=url, client=client))
            new_urls = await asyncio.gather(*urls_to_crawl)
            return new_urls

    def _collect_data(self, urls: list):
        """Fills page_details.data."""
        # Manually add first record:
        new_urls = asyncio.run(self._run(urls))
        for new_url in new_urls:
            self._collect_data(urls=new_url)

    def _save_as_csv(self, output: str):
        """Saves collected data as CSV file."""
        headers = ['url', 'title', 'internal links', 'external links', 'reference count']
        with open(output, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for detail_dict in self.page_details.data.values():
                writer.writerow(detail_dict)

    def _save_as_json(self, output: str):
        """Saves collected data as JSON file."""
        data = list(self.page_details.data.values())
        with open(output, 'w') as file:
            json.dump(data, file)

    def _search_for_links(self, url: str, request: AsyncClient.request) -> list:
        """Crawls URL and returns list of new unique URLs."""
        links_to_crawl = set()  # Set of internal links that weren't crawled yet.
        internal_links = set()  # All internal links found on current page.
        external_links = set()  # All external links found on current page.

        soup = BeautifulSoup(request.text, features='html.parser')

        title = soup.find('title')
        if title:
            self.page_details.update_title(url=url, title=title.text)

        anchors = soup.find_all('a')
        for a in anchors:
            link = a.get('href')
            try:
                # As mentioned in Task description: "For simplicity assume that external links start with http."
                external = link.startswith('http')
            except AttributeError:
                pass
            else:
                if not external:
                    # Create full link with built-in urljoin:
                    full_link = urljoin(url, link)
                    if not isinstance(validators.url(full_link), validators.ValidationFailure):
                        if full_link not in self.page_details.data:
                            self.page_details.create_record(url=full_link)
                            links_to_crawl.add(full_link)
                            internal_links.add(full_link)
                        else:
                            if full_link != url:
                                internal_links.add(full_link)

                else:
                    if not isinstance(validators.url(link), validators.ValidationFailure):
                        external_links.add(link)

        # Update links count for current page:
        self.page_details.update_links_count(url=url, internal=len(internal_links), external=len(external_links))

        # Update reference count for all internal links that were previously found on other subpages:
        for link in internal_links - links_to_crawl:
            self.page_details.update_reference_count(url=link)

        # Return the list of new URLs to crawl:
        return list(links_to_crawl)
