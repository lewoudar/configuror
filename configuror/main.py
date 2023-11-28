"""Module which holds the Config class"""
import importlib.util as import_util
import json
import os

# noinspection PyProtectedMember
from configparser import BasicInterpolation, ConfigParser, ExtendedInterpolation
from configparser import Error as IniDecodeError
from importlib import import_module
from itertools import chain
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

import toml
import yaml
from yaml.parser import ParserError as YamlParserError

from .exceptions import DecodeError, UnknownExtensionError
from .utils import convert_ini_config_to_dict, get_dict_from_dotenv_file

Object = TypeVar('Object')

JSON_TYPE = 'json'

YAML_TYPE = 'yaml'

INI_TYPE = 'ini'

TOML_TYPE = 'toml'

PYTHON_TYPE = 'python'

ENV_TYPE = 'env'

EXTENSIONS = {
    JSON_TYPE: ['json'],
    YAML_TYPE: ['yml', 'yaml'],
    INI_TYPE: ['ini', 'cfg'],
    TOML_TYPE: ['toml'],
    PYTHON_TYPE: ['py'],
    ENV_TYPE: ['env'],
}
# we create a list with all available extensions supported by configuror, it comes in handy
# for the implementation of load_from_files method
AVAILABLE_EXTENSIONS = list(chain(*[value for value in EXTENSIONS.values()]))


class Config(dict):
    def __init__(
        self,
        mapping_files: Optional[Dict[str, List[str]]] = None,
        files: Optional[List[str]] = None,
        ignore_file_absence: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._type_error_message = '{filename} is not a string representing a path'
        self.load_from_mapping_files(mapping_files, ignore_file_absence)
        self.load_from_files(files, ignore_file_absence)

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
    def getenv(key: str, default: Any = None, converter: Optional[Callable] = None) -> Any:
        value = os.getenv(key, default)
        if converter is None:
            return value

        if not callable(converter):
            raise TypeError('cast must be a callable')
        return converter(value)

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
            except AttributeError as e:
                raise DecodeError(filename, PYTHON_TYPE) from e

    def load_from_json(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._path_is_ok(filename, ignore_file_absence):
            return False

        try:
            with open(filename) as f:
                self.update(json.load(f))
        except json.JSONDecodeError as e:
            raise DecodeError(filename, JSON_TYPE) from e
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
        except YamlParserError as e:
            raise DecodeError(filename, YAML_TYPE) from e
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
        except toml.TomlDecodeError as e:
            raise DecodeError(message=f'one of your files is not well {TOML_TYPE} formatted') from e
        except FileNotFoundError as e:  # This occurs when the list is empty, I just changed the error message to return
            raise FileNotFoundError(f'the list does not contain one {TOML_TYPE} valid file') from e

    def load_from_ini(
        self, filenames: Union[str, List], ignore_file_absence: bool = False, interpolation_method: str = 'basic'
    ) -> bool:
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
            interpolation = (
                ExtendedInterpolation() if interpolation_method.lower() == 'extended' else BasicInterpolation()
            )
            config = ConfigParser(interpolation=interpolation)
            config.read(filtered_filenames)
            self.update(convert_ini_config_to_dict(config))
            return True
        except IniDecodeError as e:
            raise DecodeError(message=f'one of your files is not well {INI_TYPE} formatted') from e

    def load_from_dotenv(self, filename: str, ignore_file_absence: bool = False) -> bool:
        if not self._path_is_ok(filename, ignore_file_absence):
            return False

        data = get_dict_from_dotenv_file(filename)
        if not data:
            return False

        for key, value in data.items():
            new_value = os.path.expandvars(value)
            os.environ[key] = new_value
            self[key] = new_value
        return True

    def _load_from_mapping_file(self, file_type: str, existing_files: List[str]) -> None:
        mapping = {
            JSON_TYPE: self.load_from_json,
            YAML_TYPE: self.load_from_yaml,
            TOML_TYPE: self.load_from_toml,
            INI_TYPE: self.load_from_ini,
            PYTHON_TYPE: self.load_from_python_file,
            ENV_TYPE: self.load_from_dotenv,
        }
        if (load_callable := mapping.get(file_type)) is not None:
            if file_type in (INI_TYPE, TOML_TYPE):
                load_callable(existing_files)
            else:
                for file in existing_files:
                    load_callable(file)

    def load_from_mapping_files(
        self, mapping_files: Optional[Dict[str, List[str]]] = None, ignore_file_absence: bool = False
    ) -> bool:
        if mapping_files is None:
            return False

        file_added = False
        for key, files in mapping_files.items():
            file_type = key.lower()
            if file_type not in EXTENSIONS.keys():
                raise UnknownExtensionError(key)
            if not isinstance(files, list):
                raise TypeError(f'{files} is not a list of files')

            existing_files = self._filter_paths(files, ignore_file_absence)
            if existing_files:  # if at least one file is added, the operation is considered realized
                file_added = True
                self._load_from_mapping_file(file_type, existing_files)

        return file_added

    def _load_from_files(self, file: str, extension: str) -> None:
        if extension in EXTENSIONS[PYTHON_TYPE]:
            self.load_from_python_file(file)

        elif extension in EXTENSIONS[JSON_TYPE]:
            self.load_from_json(file)

        elif extension in EXTENSIONS[TOML_TYPE]:
            self.load_from_toml(file)

        elif extension in EXTENSIONS[INI_TYPE]:
            self.load_from_ini(file)

        elif extension in EXTENSIONS[YAML_TYPE]:
            self.load_from_yaml(file)
        else:
            self.load_from_dotenv(file)

    def load_from_files(self, filenames: Optional[List[str]] = None, ignore_file_absence: bool = False) -> bool:
        if filenames is None:
            return False
        if not isinstance(filenames, list):
            raise TypeError(f'{filenames} is not a list of files')

        files = self._filter_paths(filenames, ignore_file_absence)
        if not files:
            return False
        else:
            for file in files:
                extension = file.split('.')[-1]
                if extension not in AVAILABLE_EXTENSIONS:
                    raise UnknownExtensionError(
                        message=f'{file} does not have a correct extension,'
                        f' supported extensions are: {AVAILABLE_EXTENSIONS}'
                    )

                self._load_from_files(file, extension)
            return True

    def get_dict_from_namespace(
        self, namespace: str, lowercase: bool = True, trim_namespace: bool = True
    ) -> Dict[str, Any]:
        result_dict = {}
        for key, value in self.items():
            if not isinstance(key, str) or not key.startswith(namespace):
                continue
            if trim_namespace:
                key = key[len(namespace):]  # fmt: skip
            if lowercase:
                key = key.lower()
            result_dict[key] = value

        return result_dict
