import sys

from app.model import Model


class TestModelOutput:
    """Test Model's output related methods."""
    def test_extension_validation_OK(self):
        """Check if correct extensions are validated."""
        model = Model()
        res1 = model.is_valid_extension(extension='csv')
        res2 = model.is_valid_extension(extension='json')
        res3 = model.is_valid_extension(extension='CSV')
        res4 = model.is_valid_extension(extension='JSON')

        assert res1 is True
        assert res2 is True
        assert res3 is True
        assert res4 is True

    def test_extension_validation_wrong(self):
        """Check if invalid extensions are caught by validator."""
        model = Model()
        res1 = model.is_valid_extension(extension='Json')
        res2 = model.is_valid_extension(extension='xml')

        assert res1 is False
        assert res2 is False


class TestModelPath:
    """Test Model's path methods."""
    def test_update_output_OK(self):
        """Test if method works when used properly."""
        model = Model()
        if sys.platform != 'win32':
            path = '/home/User/output'
            extension = 'json'
            expected = '/home/User/output.json'

        else:
            path = 'C:\\User\\output'
            extension = 'json'
            expected = 'C:\\User\\output.json'

        model.update_output(path=path, extension=extension)
        res = model.output

        assert res == expected


class TestModelURL:
    """Test Model's URL methods."""
    def test_validation_OK(self):
        """Test if correct URL addresses are validated."""
        model = Model()
        res1 = model.is_valid_url(url='https://www.example.com')
        res2 = model.is_valid_url(url='http://www.example.com')
        res3 = model.is_valid_url(url='https://nowww.dev.it/projects/project')

        assert res1 is True
        assert res2 is True
        assert res3 is True

    def test_validation_wrong(self):
        """Test if incorrect URLs are caught by validator."""
        model = Model()
        res1 = model.is_valid_url(url='www.example.com')
        res2 = model.is_valid_url(url='example.com')
        res3 = model.is_valid_url(url='some string')

        assert res1 is False
        assert res2 is False
        assert res3 is False
