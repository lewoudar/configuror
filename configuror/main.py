"""Module which holds the Config class"""
import json
import os
from importlib import import_module
import importlib.util as import_util
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Union, Any

import yaml
from yaml.parser import ParserError as YamlParserError
import toml
# noinspection PyProtectedMember
from configparser import ConfigParser, Error as IniDecodeError, BasicInterpolation, ExtendedInterpolation

from .exceptions import FileTypeError, DecodeError
from .utils import convert_ini_config_to_dict

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
        self._type_error_message = '{filename} is not a string representing a path'

    @staticmethod
    def _path_is_ok(filename: str, ignore_file_absence: bool = False) -> bool:
        """
        :param filename: the filename to check for.
        :param ignore_file_absence: boolean flag to know if we raised an error if the file doesn't exist.
        :return: True if the file exists on the filesystem, False otherwise.
        """
        if os.path.isfile(filename):
            return True
        if ignore_file_absence:
            return False
        raise FileNotFoundError(f'file {filename} not found on the filesystem')

    def _filter_paths(self, filenames: List[str], ignore_file_absence: bool = False) -> List[str]:
        """
        :param filenames: list of files to check for.
        :param ignore_file_absence: boolean flag to know if we raised an error if a file in the list doesn't exist.
        :return: list of files guaranteed to exist on the filesystem.
        """
        for filename in filenames:
            if not isinstance(filename, str):
                raise TypeError(self._type_error_message.format(filename=filename))
        return [filename for filename in filenames if self._path_is_ok(filename, ignore_file_absence)]

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
            raise TypeError(self._type_error_message.format(filename=filename))

        if not self._path_is_ok(filename, ignore_file_absence):
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
        if not self._path_is_ok(filename, ignore_file_absence):
            return False

        try:
            with open(filename) as f:
                self.update(json.load(f))
        except json.JSONDecodeError:
            raise DecodeError(filename, JSON_TYPE)
        return True

    def load_from_yaml(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._path_is_ok(filename, ignore_file_absence):
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

    def load_from_toml(self, filenames: Union[str, List[str]], ignore_file_absence: bool = False) -> bool:
        if not isinstance(filenames, (str, list)):
            raise TypeError('filenames must represent a path or list of paths')
        if isinstance(filenames, str):
            if not self._path_is_ok(filenames, ignore_file_absence):
                return False
            filenames = [filenames]

        filtered_filenames = self._filter_paths(filenames, ignore_file_absence)
        try:
            self.update(toml.load(filtered_filenames))
            return True
        except toml.TomlDecodeError:
            raise DecodeError(message=f'one of your files is not well {TOML_TYPE} formatted')
        except FileNotFoundError:  # This occurs when the list is empty, I just changed the error message to return
            raise FileNotFoundError(f'the list does not contain one {TOML_TYPE} valid file')

    def load_from_ini(self, filenames: Union[str, List], ignore_file_absence: bool = False,
                      interpolation_method: str = 'basic') -> bool:
        # we check interpolation method
        interpolation_error_message = 'interpolation_method must be either "basic" or "extended"'
        if not isinstance(interpolation_method, str):
            raise TypeError(interpolation_error_message)
        if interpolation_method.lower() not in ['basic', 'extended']:
            raise ValueError(interpolation_error_message)

        # we check filenames
        if not isinstance(filenames, (str, list)):
            raise TypeError('filenames must represent a path or list of paths')
        if isinstance(filenames, str):
            if not self._path_is_ok(filenames, ignore_file_absence):
                return False
            filenames = [filenames]

        filtered_filenames = self._filter_paths(filenames, ignore_file_absence)
        try:
            interpolation = ExtendedInterpolation() if interpolation_method.lower() == 'extended' \
                else BasicInterpolation()
            config = ConfigParser(interpolation=interpolation)
            config.read(filtered_filenames)
            self.update(convert_ini_config_to_dict(config))
            return True
        except IniDecodeError:
            raise DecodeError(message=f'one of your files is not well {INI_TYPE} formatted')

    def get_dict_from_namespace(self, namespace: str, lowercase: bool = True,
                                trim_namespace: bool = True) -> Dict[str, Any]:
        result_dict = {}
        for key, value in self.items():
            if not isinstance(key, str) or not key.startswith(namespace):
                continue
            if trim_namespace:
                key = key[len(namespace):]
            if lowercase:
                key = key.lower()
            result_dict[key] = value

        return result_dict
