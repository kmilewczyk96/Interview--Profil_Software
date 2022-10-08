from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.page_details import PageDetails
from app.command_validators import CommandValidators


class Model:
    """Contains methods which execute App's CLI commands."""
    def __init__(self):
        self.page_details = PageDetails()
        self.validator = CommandValidators()

    def crawl(self, url: str, extension: str, path: str):
        """Crawls the page and its sub-pages. Exports data to provided output in one of two available extensions."""
        self.page_details.create_record(url=url, is_base=True)
        self._search_for_links(url=url)

        output = f'{path}.{extension}'
        if extension.lower() == 'csv':
            self._save_as_csv(output=output)
        if extension.lower() == 'json':
            self._save_as_json(output=output)

    def print_tree(self, url: str):
        pass

    def _save_as_csv(self, output: str):
        """Converts collected data into CSV and saves to provided output."""
        headers = ['link', 'title', 'number of internal links', 'number of external links', 'reference count']
        with open(output, 'w') as file:
            # Create headers:
            file.write(','.join(headers) + '\n')
            # For each detail dict in collected data join its values with comma.
            for detail_dict in self.page_details.data.values():
                file.write(','.join([str(i) for i in detail_dict.values()]) + '\n')

    def _save_as_json(self, output: str):
        """Converts collected data into JSON and saves to provided output."""
        pass

    def _search_for_links(self, url: str):
        """Crawls single page. Updates data for page details."""
        links_to_crawl = set()  # Set of internal links that weren't crawled yet.
        internal_links = set()  # All internal links found on current page.
        external_links = set()  # All external links found on current page.

        request = requests.get(url=url)
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
                    if full_link not in self.page_details.data:
                        self.page_details.create_record(url=full_link)
                        links_to_crawl.add(full_link)
                        internal_links.add(full_link)
                    else:
                        if full_link != url:
                            internal_links.add(full_link)

                else:
                    external_links.add(link)

        # Update links count for current page:
        self.page_details.update_links_count(url=url, internal=len(internal_links), external=len(external_links))

        # Update reference count for all internal links that were previously found on other subpages:
        for link in internal_links - links_to_crawl:
            self.page_details.update_reference_count(url=link)

        # Call this function until subpage with no new subpages is found:
        for link in links_to_crawl:
            self._search_for_links(url=link)
