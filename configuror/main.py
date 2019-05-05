"""Module which holds the Config class"""
import json
import os
from importlib import import_module
import importlib.util as import_util
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Union

import yaml
from yaml.parser import ParserError as YamlParserError

from .exceptions import FileTypeError, DecodeError

Object = TypeVar('Object')

JSON_TYPE = 'json'

YAML_TYPE = 'yaml'

INI_TYPE = 'ini'

TOML_TYPE = 'toml'

PYTHON_TYPE = 'python'

EXTENSIONS = {
    JSON_TYPE: ['json'],
    YAML_TYPE: ['yml', 'yaml'],
    INI_TYPE: ['ini', 'cfg'],
    TOML_TYPE: ['toml'],
    PYTHON_TYPE: ['py']
}


class Config(dict):

    def __init__(self, mapping_files: Dict[str, List[str]] = None, files: List[str] = None,
                 ignore_file_absence: bool = False, **kwargs):
        super(Config, self).__init__(**kwargs)

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
            raise FileTypeError(filename, file_type)

    @staticmethod
    def getenv(key: str) -> Optional[str]:
        return os.getenv(key)

    def load_from_object(self, obj: Union[Object, str]) -> None:
        if isinstance(obj, str):
            obj = import_module(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def load_from_python_file(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not isinstance(filename, str):
            raise TypeError(f'{filename} is not a string representing a path')

        if not self._is_path_ok(filename, ignore_file_absence):
            return False
        else:
            try:
                spec = import_util.spec_from_file_location(Path(filename).stem, filename)
                module = import_util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.load_from_object(module)
                return True
            except AttributeError:
                raise DecodeError(filename, PYTHON_TYPE)

    def load_from_json(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._is_path_ok(filename, ignore_file_absence):
            return False

        try:
            with open(filename) as f:
                self.update(json.load(f))
        except json.JSONDecodeError:
            raise DecodeError(filename, JSON_TYPE)
        return True

    def load_from_yaml(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._is_path_ok(filename, ignore_file_absence):
            return False

        try:
            with open(filename) as f:
                data = yaml.full_load(f)
                if not isinstance(data, dict):
                    return False
                self.update(data)
        except YamlParserError:
            raise DecodeError(filename, YAML_TYPE)
        return True
