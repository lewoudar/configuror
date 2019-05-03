class ConfigurorError(Exception):
    """base error"""
    pass


class FileTypeError(ConfigurorError):
    pass


class DecodeError(ConfigurorError):
    pass
