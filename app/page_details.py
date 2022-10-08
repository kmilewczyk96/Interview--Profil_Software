class PageDetails:
    """Handles adding and updating page's details."""
    def __init__(self):
        self.data = {}

    def create_record(self, url: str, is_base=False):
        """Creates new record for unique URL."""
        self.data[url] = {
            'url': url,
            'title': '',
            'internal links': 0,
            'external links': 0,
            'reference count': 1 if not is_base else 0
        }

    def update_links_count(self, url: str, internal: int, external: int):
        """Updates specific page links count by passed value."""
        if internal or external:
            self.data[url]['internal links'] += internal
            self.data[url]['external links'] += external

    def update_reference_count(self, url: str):
        """Increases specific page reference count by 1."""
        self.data[url]['reference count'] += 1

    def update_title(self, url: str, title: str):
        """Updates page title."""
        self.data[url]['title'] = title
