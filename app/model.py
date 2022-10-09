import csv
import json
from urllib.parse import urljoin

import requests
import typer
import validators
from bs4 import BeautifulSoup

from app.page_details import PageDetails
from app.command_validators import CommandValidators
from app.utils import count_time_execution


class Model:
    """Contains methods which execute App's CLI commands."""

    def __init__(self):
        self.page_details = PageDetails()
        self.validator = CommandValidators()

    @count_time_execution
    def crawl(self, url: str, extension: str, path: str):
        """Crawls the page and its subpages. Exports data to provided output in one of two available extensions."""
        self._collect_data(url=url)
        output = f'{path}.{extension}'
        if extension.lower() == 'csv':
            self._save_as_csv(output=output)
        if extension.lower() == 'json':
            self._save_as_json(output=output)

    def print_tree(self, url: str) -> list:
        """
        Crawls the page and its subpages.
        Returns list of dicts, which contain: URLs, their indentation and subpages count.
        """
        self._collect_data(url=url)
        urls = [url for url in self.page_details.data]
        # Sort urls by the indentation:
        urls.sort(key=lambda x: x.count('/'))

        excluded = []
        tree = []

        def _search_for_children(current_url, indentation=0):
            subpages_count = 0
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

    def _collect_data(self, url):
        """Fills page_details.data."""
        # Manually add first record:
        self.page_details.create_record(url=url, is_base=True)
        self._search_for_links(url=url)

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

    def _search_for_links(self, url: str):
        typer.echo(f'Checking URL: {url}')
        """Crawls subpages until it can't find new internal links."""
        links_to_crawl = set()  # Set of internal links that weren't crawled yet.
        internal_links = set()  # All internal links found on current page.
        external_links = set()  # All external links found on current page.

        request = requests.get(url=url, allow_redirects=False)
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

        # Call this function until subpage with no new subpages is found:
        for link in links_to_crawl:
            self._search_for_links(url=link)
