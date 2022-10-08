from typer.testing import CliRunner

from app.cli import CommandLineInterface
from app.model import Model


class TestBaseCommands:
    model = Model()
    app = CommandLineInterface(model=model)
    runner = CliRunner()

    # Crawl command:
    def test_crawl_basic(self):
        """Tests if 'crawl' command exists."""
        res = self.runner.invoke(self.app, ['crawl', '--page', 'https://www.example.com'])
        assert res.exit_code == 0

    def test_crawl_page_required(self):
        """Tests if 'crawl' command throws error without 'page' option."""
        res = self.runner.invoke(self.app, ['crawl'])
        assert res.exit_code != 0

    def test_crawl_page_option_no_value(self):
        """Tests if 'crawl' command throws error when 'page' option takes no parameter."""
        res = self.runner.invoke(self.app, ['crawl', '--page'])
        assert res.exit_code != 0

    # Print-tree command:
    def test_print_basic(self):
        """Tests if 'print-tree' command exists."""
        res = self.runner.invoke(self.app, ['print-tree', '--page', 'https://www.example.com'])
        assert res.exit_code == 0

    def test_print_page_required(self):
        """Tests if 'print' command throws error without 'page' option."""
        res = self.runner.invoke(self.app, ['print-tree'])
        assert res.exit_code != 0

    def test_print_page_option_no_value(self):
        """Tests if 'print-tree' command throws error when 'page' option takes no parameter."""
        res = self.runner.invoke(self.app, ['print-tree', '--page'])
        assert res.exit_code != 0
