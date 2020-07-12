"""Helper functions for the project"""
import re
from configparser import ConfigParser
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Union

from .exceptions import DecodeError

SET_EXPORT_EXPRESSION = re.compile(r'[\w/]*\s*(set|export)\s+', flags=re.IGNORECASE)
ITEM_EXPRESSION = re.compile(r'[\w/]+')


def convert_ini_config_to_dict(config: ConfigParser) -> dict:
    """Translates a configparser object into a dict."""
    return {key: dict(value) for key, value in config.items()}


# DOTENV

def _sanitize_key_and_value(items: List[str]) -> List[str]:
    """Removes unwanted characters on key and value"""
    # if there are more than two items, we return the list unchanged, so an error will be raised later
    if len(items) != 2:
        return items
    key, value = items
    key = key.rstrip()
    value = value.lstrip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return [key, value]


def get_dict_from_dotenv_file(filename: Union[Path, str]) -> Dict[str, str]:
    """
    :param filename: .env file where values are extracted.
    :return: a dict with keys and values extracted from the .env file.
    """
    result_dict = {}

    error_message = 'file {filename}: the line n°{index} is not correct: "{line}"'
    with open(filename) as f:
        for index, line in enumerate(f):
            stripped_line = line.strip()
            # we don't take into account comments
            if stripped_line.startswith('#'):
                continue
            # we don't take into account empty lines
            if not stripped_line:
                continue
            parts = stripped_line.split('#')  # we remove inline comments if there are any
            # we remove set or export command if there are any
            new_line = SET_EXPORT_EXPRESSION.sub('', parts[0].strip())

            # we get key and value
            parts = new_line.split('=')
            parts = _sanitize_key_and_value(parts)
            if len(parts) != 2 or ITEM_EXPRESSION.match(parts[0]) is None \
                    or ITEM_EXPRESSION.match(parts[1]) is None:
                line_number = index + 1
                raise DecodeError(message=error_message.format(filename=filename, index=line_number, line=new_line))
            result_dict[parts[0]] = parts[1]

    return result_dict


def bool_converter(value: str) -> bool:
    """
    :param value: a string to convert to bool.
    :return: False if lower case value in "0", "n", "no" and "false", otherwise, returns the value returned
    by the bool builtin function.
    """
    if value.lower() in ['n', '0', 'no', 'false']:
        return False
    return bool(value)


def string_list(value: str) -> List[str]:
    """
    :param value: a string to convert to a list of strings. Possible separators are space, ";", "," and ":".
    Note that separators other than space can be followed by one or more... spaces!
    :return: a list of strings.
    """
    return re.split(r',\s*|;\s*|:\s*|\s+', value)


def int_list(value: str) -> List[int]:
    """
    :param value: a string to convert to a list of int. Possible separators are space, ";", "," and ":".
    Note that separators other than space can be followed by one or more... spaces!
    :return: a list of int.
    """
    return [int(item) for item in string_list(value)]


def float_list(value: str) -> List[float]:
    """
    :param value: a string to convert to a list of float. Possible separators are space, ";", "," and ":".
    Note that separators other than space can be followed by one or more... spaces!
    :return: a list of float.
    """
    return [float(item) for item in string_list(value)]


def decimal_list(value: str) -> List[Decimal]:
    """
    :param value: a string to convert to a list of decimal.Decimal . Possible separators are space, ";", "," and ":".
    Note that separators other than space can be followed by one or more... spaces!
    :return: a list of decimal.Decimal .
    """
    return [Decimal(item) for item in string_list(value)]


def path_list(value: str) -> List[Path]:
    """
    :param value: a string to convert to a list of pathlib.Path . Possible separators are space, ";", "," and ":".
    Note that separators other than space can be followed by one or more... spaces!
    :return: a list of pathlib.Path .
    """
    return [Path(item) for item in string_list(value)]
