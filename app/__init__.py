__app_name__ = 'app'


(
    SUCCESS,
    EXTENSION_ERROR,
    PATH_ERROR,
    URL_ERROR,
) = range(4)

ERRORS = {
    EXTENSION_ERROR: 'ERROR: Provided format is not supported.',
    PATH_ERROR: 'ERROR: Provided output path is invalid.',
    URL_ERROR: 'ERROR: Provided page URL is invalid.',
}
