class ConfigurorError(Exception):
    """base error"""


class FileTypeError(ConfigurorError):
    def __init__(self, filename: str, file_type: str):
        super().__init__(f'{filename} is not a {file_type} file')


class DecodeError(ConfigurorError):
    def __init__(self, filename: str = 'the file', file_type: str = '', message: str = None):
        error_message = message or f'{filename} is not well {file_type} formatted'
        super().__init__(error_message)
