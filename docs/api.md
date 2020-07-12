# API

[TOC]

## Constants

### `JSON_TYPE`
A string representing the json type.

### `YAML_TYPE`
A string representing the yaml type.

### `TOML_TYPE`
A string representing the toml type.

### `INI_TYPE`
A string representing the ini type.

### `DOTENV_TYPE`
A string representing the dotenv type.

### `PYTHON_TYPE`
A string representing the python type.

### `EXTENSIONS`
A dict where the *key* is a file type (the types listed above) and the value is the list of extensions supported for
this file type.

## Config

### `__init__`

Signature: `(self, mapping_files: Dict[str, List[str]] = None, files: List[str] = None, ignore_file_absence: bool = False, **kwargs)`

Parameters:

- `mapping_files`: A mapping where the _key_ is the type of the file and the _value_ is the list of files to be loaded
from the lowest to the highest priority.
- `files`: A list of files to be loaded from the lowest to the highest priority. The file extension is **mandatory** here
unlike the previous parameter.
- `ignore_file_absence`: If set to `False`, when a file in the list does not exist, a `FileNotFoundError` will
be raised. If set to `True`, no exception will be raised. By default, it is `False`.
- `kwargs`: keyword arguments which will be added as default values to the Config object.

### `getenv`

Signature: `getenv(key: str, default: Any = None, converter: Callable = None) -> Any`

Retrieves an environment variable. If the variable does not exist, it returns the default value which is None by default.

It also accepts a converter callable to convert the string to a suitable variable. There are some [examples](#utils)
further down the page.

Parameters:

- `key`: The name of the environment variable.

### `load_from_object`

Signature: `load_from_object(obj: Union[Object, str]) -> None`

Loads values from a python object or a string corresponding to a path of a module (dotted notation). 
Only **uppercase** attributes of the corresponding object will be loaded.

Parameters:

- `obj`: It can be an object (other than a dict) or a string representing a path to a project module with dotted
notation.

### `load_from_python_file`

Signature: `load_from_python_file(filename: str, ignore_file_absence: bool = False) -> bool`

Loads values from an arbitrary python file. Ideally the python file must be outside the project. Only **uppercase**
attributes of the module will be loaded. It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filename`: The path to the python file.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised, if `False` an error will be raised. It
is `False` by default.

### `load_from_json`

Signature: `load_from_json(filename: str, ignore_file_absence: bool = False) -> bool`

Loads values from a json file. **Uppercase and lowercase** attributes will be loaded.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filename`: The path to the json file.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised, if `False` an error will be raised. It
is `False` by default.

### `load_from_yaml`

Signature: `load_from_yaml(filename: str, ignore_file_absence: bool = False) -> bool`

Loads values from a yaml file. **Uppercase and lowercase** attributes will be loaded.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filename`: The path to the yaml file.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised, if `False` an error will be raised. It
is `False` by default.

### `load_from_toml`

Signature: `load_from_toml(filenames: Union[str, List[str]], ignore_file_absence: bool = False) -> bool:`

Loads values from a single toml file or a list of toml files. **Uppercase and lowercase** attributes will be loaded.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filenames`: It can be a path to a toml file or a list of toml file paths.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised if a file does not exist, if `False` 
an error will be raised. It is `False` by default.

### `load_from_ini`

Signature: `load_from_ini(filenames: Union[str, List], ignore_file_absence: bool = False, interpolation_method: str = 'basic') -> bool:`

Loads values from a single ini file or a list of ini files. **Uppercase and lowercase** attributes will be loaded.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filenames`: It can be a path to an ini file or a list of ini file paths.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised if a file does not exist, if `False` 
an error will be raised. It is `False` by default.
- `interpolation_method`: A string that can take the value `basic` or `extended`. It represents the
[interpolation](https://docs.python.org/3/library/configparser.html#interpolation-of-values) used to load values.

### `load_from_dotenv`

Signature: `load_from_dotenv(filename: str, ignore_file_absence: bool = False) -> bool`

Loads values from a dotenv file. The lines of the file can start with an optional `export` or `set` command which will
be ignored when parsing. It comes in handy when you want to use the file as a PowerShell or bash script.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filename`: The path to the dotenv file.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised, if `False` an error will be raised. It
is `False` by default.

### `load_from_mapping_files`

Signature: `load_from_mapping_files(mapping_files: Dict[str, List[str]] = None, ignore_file_absence: bool = False) -> bool`

Loads values from a mapping of files. It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `mapping_files`: A mapping where the _key_ is the type of the file and the _value_ is the list of files to be loaded
from the lowest to the highest priority.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised if a file does not exist, if `False` 
an error will be raised. It is `False` by default.

### `load_from_files`

Signature: `load_from_files(filenames: List[str] = None, ignore_file_absence: bool = False) -> bool`

Loads values from a list of files. The files must end with an **extension supported by configuror**.
You can look the variable [EXTENSIONS](#extensions) to know all valid file formats and extensions.
It returns `True` if the operation was successful and `False` otherwise.

Parameters:

- `filenames`: A list of files to be loaded from the lowest to the highest priority.
- `ignore_file_absence`: If set to `True`, no `FileNotFoundError` will be raised if a file does not exist, if `False` 
an error will be raised. It is `False` by default.

### `get_dict_from_namespace`

Signature: `get_dict_from_namespace(namespace: str, lowercase: bool = True, trim_namespace: bool = True) -> Dict[str, Any]`

Returns a dictionary that contains a subset of configuration options that matched the specified namespace.

Parameters:

- `namespace`: A configuration namespace.
- `trim_namespace`: A flag indicating if the keys of the resulting dictionary should not include the namespace.
It is `True` by default.
- `lowercase`: A flag indicating if the keys of the resulting dictionary should be lowercase. It is `True` by default.

## Utils

These functions are especially useful in combination with [Config.getenv](#getenv).

### bool_converter

Signature: `bool_converter(value: str) -> bool`

It is a convenient wrapper around the `bool` builtin function that converts string `no`, `n`, `0`, `false` to False. Those
values are case-insensitive. Other values are passed to `bool` function.

```python
from configuror import Config, bool_converter
# assuming we set environment variable DEBUG to no
config = Config()
debug = config.getenv('DEBUG', converter=bool_converter)  # debug is False
```

### string_list

Signature: `string_list(value: str) -> List[str]`

Converts a string to convert to a list of strings. Possible separators are space, `;`, `,` and `:`. Note that separators
other than space can be followed by one or more... spaces!

```python
from configuror import Config, string_list
# assuming we set environment variable FRUITS to "bananas, pineapples"
config = Config()
fruits = config.getenv('FRUITS', converter=string_list)  # fruits = ['bananas', 'pineapples']
```

### int_list

Signature: `int_list(value: str) -> List[int]`

Converts a string to convert to a list of integers. Possible separators are space, `;`, `,` and `:`. Note that 
separators other than space can be followed by one or more... spaces!

```python
from configuror import Config, int_list
# assuming we set environment variable VALUES to "2, 5, 7"
config = Config()
values = config.getenv('VALUES', converter=int_list)  # values = [2, 5, 7]
```

### float_list

Signature: `float_list(value: str) -> List[float]`

Converts a string to convert to a list of floats. Possible separators are space, `;`, `,` and `:`. Note that 
separators other than space can be followed by one or more... spaces!

```python
from configuror import Config, float_list
# assuming we set environment variable VALUES to "3, 5.2"
config = Config()
values = config.getenv('VALUES', converter=float_list)  # values = [3.0, 5.2]
```

### decimal_list

Signature: `decimal_list(value: str) -> List[Decimal]`

Converts a string to convert to a list of [Decimal](https://docs.python.org/3/library/decimal.html). Possible separators
are space, `;`, `,` and `:`. Note that separators other than space can be followed by one or more... spaces!

```python
from configuror import Config, decimal_list
# assuming we set environment variable VALUES to "3; 5.2"
config = Config()
values = config.getenv('VALUES', converter=decimal_list)  # values = [Decimal('3'), Decimal('5.2')]
```

### path_list

Signature: `path_list(value: str) -> List[Path]`

Converts a string to convert to a list of [Path](https://docs.python.org/3/library/pathlib.html). Possible separators
are space, `;`, `,` and `:`. Note that separators other than space can be followed by one or more... spaces!

```python
from configuror import Config, path_list
# assuming we set environment variable PATHS to "/tmp/bar:/usr/bin/python"
config = Config()
paths = config.getenv('PATHS', converter=path_list)  # paths = [Path('/tmp/bar'), Path('/usr/bin/python')]
```

## Exceptions

### `ConfigurorError`

The base exception.

### `DecodeError`

This exception is raised when a file cannot be decode in a given format.

### `UnknownExtensionError`

This exception is raised when a file extension is not supported.