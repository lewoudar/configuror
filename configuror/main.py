"""Module which holds the Config class"""
import json
import os
from importlib import import_module
from typing import Dict, List, Optional, TypeVar, Union

from .exceptions import FileTypeError, DecodeError

Object = TypeVar('Object')

JSON_TYPE = 'json'

YAML_TYPE = 'yaml'

INI_TYPE = 'ini'

TOML_TYPE = 'toml'

EXTENSIONS = {
    JSON_TYPE: ['json'],
    YAML_TYPE: ['yml', 'yaml'],
    INI_TYPE: ['ini', 'cfg'],
    TOML_TYPE: ['toml']
}


class Config(dict):

    def __init__(self, mapping_files: Dict[str, List[str]] = None, files: List[str] = None,
                 ignore_file_absence: bool = False, **kwargs):
        super(Config, self).__init__(**kwargs)
        self._decode_error_message = '{filename} is not well {file_type} formatted'

    @staticmethod
    def _is_path_ok(filename: str, ignore_file_absence: bool = False) -> bool:
        """Checks if we can read a file."""
        if os.path.isfile(filename):
            return True
        if ignore_file_absence:
            return False
        raise FileNotFoundError(f'file {filename} not found')

    @staticmethod
    def _check_file_type(filename: str, file_type: str) -> None:
        if filename.split('.')[-1] not in EXTENSIONS[file_type]:
            raise FileTypeError(f'{filename} is not a {file_type} file')

    @staticmethod
    def getenv(key: str) -> Optional[str]:
        return os.getenv(key)

    def load_from_object(self, obj: Union[Object, str]) -> None:
        if isinstance(obj, str):
            obj = import_module(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def load_from_json(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._is_path_ok(filename, ignore_file_absence):
            return False

        try:
            with open(filename) as f:
                self.update(json.load(f))
        except json.JSONDecodeError:
            raise DecodeError(self._decode_error_message.format(filename=filename, file_type=JSON_TYPE))
        return True
