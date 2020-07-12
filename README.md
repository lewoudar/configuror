# configuror

[![Pypi version](https://img.shields.io/pypi/v/configuror.svg)](https://pypi.org/project/configuror/)
[![Build Status](https://travis-ci.com/lewoudar/configuror.svg?branch=master)](https://travis-ci.com/lewoudar/configuror)
[![Windows Build Status](https://img.shields.io/appveyor/ci/lewoudar/configuror/master.svg?label=Windows)](https://ci.appveyor.com/project/lewoudar/configuror)
[![Coverage Status](https://codecov.io/gh/lewoudar/configuror/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/lewoudar/configuror)
[![Documentation Status](https://readthedocs.org/projects/configuror/badge/?version=latest)](https://configuror.readthedocs.io/en/latest/?badge=latest)
[![License Apache 2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)

Your configuration management toolkit!

## Why?

While using [Flask](http://flask.pocoo.org/docs/1.0/), I realized that their Config class could be useful for any type
of project. And the utility became more and more obvious to me when I looked at a project like
[Ansible](https://docs.ansible.com/ansible/latest/index.html). If you look the 
[section](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)
where they define variable precedence, you will notice that there may be several locations for the configuration files,
and these configuration files can be written in different formats (json, yaml..).

What if there was a simple tool that would aggregate information from different sources in the order you wanted? This
is **why** the configuror project exists!

## Installation

```bash
pip install configuror
```

configuror works starting from **python 3.6**. It has a few dependencies:
- [pyyaml](https://pypi.org/project/PyYAML/) >= 5.1
- [toml](https://pypi.org/project/toml/)

## Documentation

The documentation is available at https://configuror.readthedocs.io/en/latest/.

## Usage

The main class provided by configuror is `Config`. It is an extension of a regular dict object. There are two main ways 
to initialize it.

### Using mapping files

```python
from configuror import Config

mapping_files = {
    'ini': ['foo.ini', 'bar.ini'],
    'toml': ['foo.toml', 'bar.toml'],
    'python': ['/path/to/python/file']
}
config = Config(mapping_files=mapping_files, ignore_file_absence=True)
```

You can define a mapping of `file_type: <files>` where the `file_type` is the type of configuration file and `<files>` 
is the list of files from the lowest to the highest priority where values will be loaded.

Since dictionaries are sorted starting from python3.6, the order of the keys is important as it will become the order of
importance of your files. For example in the example above, configuror will load values from files in the following order:
- foo.ini
- bar.ini
- foo.toml
- bar.toml
- /path/to/python/file

For python files, only **uppercase** variables will be loaded.

You will notice the keyword argument `ignore_file_absence` in `Config` class initialization. If it is set to `True`, all
files that does not exist will not raised `FileNotFoundError`. It comes in handy when you want to retrieve variables 
from files *that may or may not potentially exist*. By default this parameter is set to `False`.

File extension is not necessary when you use mapping files since the key is already telling which files we work with.
This is not the case with the second way to initialize `Config` class.

### Using a list of files

```python
from configuror import Config

files = [
    'foo.yml',
    'bar.toml',
    'foobar.json',
    '/path/to/python/file'
    '.env'
]
config = Config(files=files)
```

In this second form of initialization, you pass a list of files you want to retrieve values from the lowest to the
highest priority. File extension is **mandatory** here to help configuror to load the files properly.

To know file extensions supported by configuror, you can use the variable `EXTENSIONS`. it is a mapping
`file_type: <extensions>` where `file_type` is a type of file supported like *yaml* and `extensions` is a list of
recognized extensions for this type of file, e.g: `[yml, yaml]`

Today the file types supported are *toml*, *yaml*, *dotenv*, *ini*, *python* and *json*.

### Other usages

Since `Config` object is a dict-like object, you can pass arbitrary keyword arguments to initialize default values.

```python
from configuror import Config

config = Config(FOO=2, BAR='a')
print(config)  # will print {'FOO': 2, 'BAR': 'a'}
```

You can combine keyword arguments, mapping files and list of files at initialization. The order in which values will be
initialized is the following:
- values from keyword arguments
- values from mapping files
- values from list of files

You can also add values from files after initialization. There are several practical methods for this:
- `load_from_mapping_files(self, mapping_files: Dict[str, List[str]], ignore_file_absence: bool)`: It is in fact the 
method used under the hood when you initialized `Config` object by passing the parameter `mapping_files`.

- `load_from_files(self, files: List[str], ignore_file_absence: bool)`: It is the method used under the hood when you
initialized `Config` objects by passing the parameter `files`. 

- `load_from_object(self, obj: Union[Object, str])`: `obj` can be an object or a path to a project module
(with dotted notation). Only uppercase attributes of the corresponding object will be retrieved.

- `load_from_python_file(self, filename: str, ignore_file_absence: bool)`: Loads values from an arbitrary python
file. It would be preferable if it were not a file related to your project (i.e a module). Only uppercase variables
are considered.

- `load_from_json(self, filename: str, ignore_file_absence: bool)`: Loads values from a json file.

- `load_from_yaml(self, filename: str, ignore_file_absence: bool)`: Loads values from a yaml file.

- `load_from_toml(self, filenames: Union[str, List[str]], ignore_file_absence: bool)`: Loads values from a toml file
or a list of toml files.

- `load_from_ini(self, filenames: Union[str, List], ignore_file_absence: bool, interpolation_method: str = 'basic')`:
Loads values from an ini file or a list of ini files. There are two interpolation methods that can be used: **basic** 
or **extended** like explained in the
[documentation](https://docs.python.org/3/library/configparser.html#interpolation-of-values).

- `load_from_dotenv(self, filename: str, ignore_file_absence: bool)`: Loads values from a dotenv file.

Bonus: You also have the `update` method of a dict to add/update values.
