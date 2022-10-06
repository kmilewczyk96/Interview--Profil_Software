import os
import re

import requests
import typer
import validators
from bs4 import BeautifulSoup

from app import __app_name__


class Model:
    def __init__(self):
        self.base_URL = ''
        self.internal_URLs = []
        self.external_URLs = []
        self.output = ''

    @staticmethod
    def get_info(bool_: bool):
        if bool_:
            typer.echo(f'{__app_name__} - simple web crawler.')
            raise typer.Exit()

    @staticmethod
    def is_valid_extension(extension: str) -> bool:
        """Check if passed extension is valid, returns boolean value."""
        check = extension in ('csv', 'CSV', 'json', 'JSON')
        return check

    @staticmethod
    def is_valid_path(path: str) -> bool:
        """Check if passed path is valid, returns boolean value."""
        # Check if path is absolute:
        if not path == os.path.abspath(path):
            return False
        # Check if directory exists:
        if not os.path.isdir(os.path.dirname(path)):
            return False
        # Check if file name doesn't have invalid characters for Windows:
        if not re.fullmatch(r'[^\\/:*?"<>|]*', os.path.basename(path)):
            return False

        return True

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if passed URL is valid, returns boolean value."""
        check = validators.url(url)
        if isinstance(check, validators.ValidationFailure):
            return False

        return True

    def update_output(self, path: str, extension: str):
        self.output = os.path.abspath(f'{path}.{extension}')
