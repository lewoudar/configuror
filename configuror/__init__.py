__version__ = '0.1.0'

from .main import Config, JSON_TYPE, YAML_TYPE, ENV_TYPE, TOML_TYPE, PYTHON_TYPE, INI_TYPE, EXTENSIONS
from .exceptions import FileTypeError, DecodeError, UnknownExtensionError

__all__ = [
    # main
    'Config', 'JSON_TYPE', 'YAML_TYPE', 'ENV_TYPE', 'TOML_TYPE', 'PYTHON_TYPE', 'INI_TYPE', 'EXTENSIONS',

    # exceptions
    'FileTypeError', 'DecodeError', 'UnknownExtensionError'
]
