import os

import typer

from app import (
    ERRORS,
    EXTENSION_ERROR,
    PATH_ERROR,
    URL_ERROR
)
from app.model import Model


class CommandLineInterface(typer.Typer):
    def __init__(self, model: Model):
        super().__init__()
        self._model = model
        self._create_commands()

    def _create_commands(self):
        """Add commands to CLI."""
        @self.command('crawl')
        def crawl(
                url: str = typer.Option(
                    ...,  # <- sets option as required one.
                    '--page',
                    help='A full URL you\'d like to crawl.'
                ),
                extension: str = typer.Option(
                    'json',
                    '--format',
                    help='Format in which the output would be saved.'
                ),
                path: str = typer.Option(
                    os.path.join(os.getcwd(), 'output'),
                    '--output',
                    help='An absolute path to the output file. The extension will be provided by program!'
                )
        ) -> None:
            if not self._model.validator.is_valid_url(url=url):
                typer.secho(ERRORS[URL_ERROR], fg=typer.colors.RED)

            if not self._model.validator.is_valid_extension(extension=extension):
                typer.secho(ERRORS[EXTENSION_ERROR], fg=typer.colors.RED)

            if not self._model.validator.is_valid_path(path=path):
                typer.secho(ERRORS[PATH_ERROR], fg=typer.colors.RED)

            if not self._model.validator.valid:
                return None

            typer.echo('All command validations passed. Proceeding...')
            self._model.crawl(url=url, extension=extension, path=path)

            return None

        @self.command('print-tree')
        def print_tree(
                url: str = typer.Option(
                    ...,
                    '--page',
                    help='A full URL you\'d like to get tree of.'
                )
        ) -> None:
            if not self._model.validator.is_valid_url(url=url):
                typer.secho(ERRORS[URL_ERROR], fg=typer.colors.RED)

            if not self._model.validator.valid:
                return None

            tree_dict = self._model.print_tree(url=url)
            typer.echo('Printing tree:')
            for branch in tree_dict:
                typer.echo(
                    f"{branch['indentation'] * '    '}{branch['url']}  ({branch['subpages_count']})"
                )

            return None
