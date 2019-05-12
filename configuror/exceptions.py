class ConfigurorError(Exception):
    """base error"""


class DecodeError(ConfigurorError):
    def __init__(self, filename: str = 'the file', file_type: str = '', message: str = None):
        error_message = message or f'{filename} is not well {file_type} formatted'
        super().__init__(error_message)


class UnknownExtensionError(ConfigurorError):
    def __init__(self, extension: str = '', message: str = None):
        error_message = message or f'extension "{extension}" is not supported'
        super().__init__(error_message)
