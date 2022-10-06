import os
import sys

import typer
from typing import Optional

from app import (
    __app_name__,
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
                page: str = typer.Option(
                    ...,  # <- sets option as required one.
                    '--page',
                    help='A full URL you\'d like to crawl.'
                ),
                format_: str = typer.Option(
                    'json',
                    '--format',
                    help='Format in which the output would be saved.'
                ),
                output: str = typer.Option(
                    os.path.join(os.getcwd(), 'output'),
                    '--output',
                    help='A path to the output file. An extension will be provided by program!'
                )
        ) -> None:
            if self._model.is_valid_url(url=page):
                pass
            else:
                typer.secho(ERRORS[URL_ERROR], fg=typer.colors.RED)
                return None

            if self._model.is_valid_extension(extension=format_):
                pass
            else:
                typer.secho(ERRORS[EXTENSION_ERROR], fg=typer.colors.RED)
                return None

            if self._model.is_valid_path(path=output):
                pass
            else:
                typer.secho(ERRORS[PATH_ERROR], fg=typer.colors.RED)
                return None

            return None

        @self.command('print-tree')
        def print_tree(
                page: str = typer.Option(
                    ...,
                    '--page',
                    help='A full URL you\'d like to get tree of.'
                )
        ) -> None:
            if self._model.is_valid_url(url=page):
                pass
            else:
                typer.secho(ERRORS[URL_ERROR], fg=typer.colors.RED)

            return None
