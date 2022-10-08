import os
import re

import validators


class CommandValidators:
    """Contains validation methods."""
    def __init__(self):
        self.valid = True

    def is_valid_extension(self, extension: str) -> bool:
        """Checks if passed extension is valid."""
        check = extension in ('csv', 'CSV', 'json', 'JSON')
        if not check:
            self.valid = False
            return False

        return True

    def is_valid_path(self, path: str) -> bool:
        """Checks if passed path is valid."""
        # Check if path is absolute:
        if not path == os.path.abspath(path):
            self.valid = False
            return False
        # Check if directory exists:
        if not os.path.isdir(os.path.dirname(path)):
            self.valid = False
            return False
        # Check if file name doesn't have invalid characters for Windows:
        if not re.fullmatch(r'[^\\/:*?"<>|]*', os.path.basename(path)):
            self.valid = False
            return False

        return True

    def is_valid_url(self, url: str) -> bool:
        """Checks if passed URL is valid."""
        check = validators.url(url)
        if isinstance(check, validators.ValidationFailure):
            self.valid = False
            return False

        return True
