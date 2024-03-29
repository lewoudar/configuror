"""Tests util module"""
from configparser import ConfigParser
from decimal import Decimal
from pathlib import Path

import pytest

from configuror.exceptions import DecodeError

# noinspection PyProtectedMember
from configuror.utils import (
    _sanitize_key_and_value,
    bool_converter,
    convert_ini_config_to_dict,
    decimal_list,
    float_list,
    get_dict_from_dotenv_file,
    int_list,
    path_list,
    string_list,
)


@pytest.fixture()
def configparser():
    return ConfigParser()


class TestConvertIniConfigToDict:
    """tests function convert_ini_config_to_dict"""

    def test_should_return_dict_with_empty_default_section_when_ini_file_is_empty(self, tmp_path, configparser):
        path = tmp_path / 'test.ini'
        path.touch()
        configparser.read(f'{path}')
        result_dict = convert_ini_config_to_dict(configparser)

        assert 1 == len(result_dict)
        assert {} == result_dict['DEFAULT']

    def test_should_return_correct_dict_when_passing_configparser_object(self, configparser):
        configparser.read('dummy.ini')
        result_dict = convert_ini_config_to_dict(configparser)

        for item in ['databases', 'servers.alpha', 'servers.beta']:
            assert item in result_dict
        assert '192.168.1.1' == result_dict['databases']['server']


class TestSanitizeKeyAndValue:
    """Tests function _sanitize_key_and_value"""

    @pytest.mark.parametrize('items', [[], ['foo'], ['foo', 'bar', 'char']])
    def test_should_return_the_same_list_if_items_length_is_not_equal_to_two(self, items):
        assert items == _sanitize_key_and_value(items)

    @pytest.mark.parametrize(
        ('given_items', 'expected_items'),
        [
            (['key', 'value'], ['key', 'value']),
            (['key  ', '  value'], ['key', 'value']),
            (['key', "o'clock"], ['key', "o'clock"]),
            (['key', '"o\'clock"'], ['key', "o'clock"]),
            (['key', "'Big Mom'"], ['key', 'Big Mom']),
        ],
    )
    def test_should_return_correct_sanitized_items(self, given_items, expected_items):
        assert expected_items == _sanitize_key_and_value(given_items)


class TestGetDictFromDotEnvFile:
    """tests function get_dict_from_dotenv_file"""

    def test_should_return_correct_dict_when_parsing_dotenv_file(self, tmp_path):
        content_lines = [
            '# a first comment',
            'set foo=bar',
            'char = var',
            '     ',
            'EXPORT tic =tac  # a second comment',
            '# another comment',
            'SET_FOO  = CLIMB',
            'exportCHAR=  paint',
            '  too = much ',
            'NAME="Kevin T"',
        ]
        expected_dict = {
            'foo': 'bar',
            'char': 'var',
            'tic': 'tac',
            'SET_FOO': 'CLIMB',
            'exportCHAR': 'paint',
            'too': 'much',
            'NAME': 'Kevin T',
        }
        path = tmp_path / '.env'
        path.write_text('\n'.join(content_lines))

        assert expected_dict == get_dict_from_dotenv_file(path)

    @pytest.mark.parametrize('invalid_line', ['set=foo=bar', 'foo =', '= bar'])
    def test_should_raise_error_when_syntax_is_incorrect(self, tmp_path, invalid_line):
        content_lines = ['export NAME=FOO', invalid_line]
        path = tmp_path / '.env'
        path.write_text('\n'.join(content_lines))

        with pytest.raises(DecodeError) as exc_info:
            get_dict_from_dotenv_file(path)

        assert f'file {path}: the line n°2 is not correct: "{invalid_line}"' == str(exc_info.value)


class TestBoolConverter:
    """Tests function bool_converter"""

    @pytest.mark.parametrize('value', ['no', '0', 'False', 'N', 'n'])
    def test_should_return_false_when_giving_appropriate_value(self, value):
        assert bool_converter(value) is False

    @pytest.mark.parametrize('value', ['yo', 'True', '1'])
    def test_should_return_true_for_any_other_value(self, value):
        assert bool_converter(value) is True


@pytest.mark.parametrize(
    ('given', 'expected'),
    [
        ('foo', ['foo']),
        ('foo:bar', ['foo', 'bar']),
        ('foo,bar', ['foo', 'bar']),
        ('foo bar', ['foo', 'bar']),
        ('foo; bar', ['foo', 'bar']),
    ],
)
def test_string_list(given, expected):
    """Tests function string_list"""
    assert expected == string_list(given)


class TestIntList:
    """Tests function int_list"""

    def test_should_call_string_list_function(self, mocker):
        data = '1, 2, 3'
        string_list_mock = mocker.patch('configuror.utils.string_list', return_value=[])
        int_list(data)
        string_list_mock.assert_called_once_with(data)

    def test_should_return_int_list_when_giving_correct_input(self):
        assert [1, 2, 3] == int_list('1, 2, 3')


class TestFloatList:
    """Tests function float_list"""

    def test_should_call_string_list_function(self, mocker):
        data = '1, 3.2'
        string_list_mock = mocker.patch('configuror.utils.string_list', return_value=[])
        float_list(data)
        string_list_mock.assert_called_once_with(data)

    def test_should_return_float_list_when_giving_correct_input(self):
        assert [1.0, 3.2] == float_list('1, 3.2')


class TestDecimalList:
    """Tests function decimal_list"""

    def test_should_call_string_list_function(self, mocker):
        data = '1; 3.2'
        string_list_mock = mocker.patch('configuror.utils.string_list', return_value=[])
        decimal_list(data)
        string_list_mock.assert_called_once_with(data)

    def test_should_return_decimal_list_when_giving_correct_input(self):
        assert [Decimal('1'), Decimal('3.2')] == decimal_list('1; 3.2')


class TestPathList:
    """Tests function path_list"""

    def test_should_call_string_list_function(self, mocker):
        data = '/tmp/bar:/usr/bin/python'
        string_list_mock = mocker.patch('configuror.utils.string_list', return_value=[])
        path_list(data)
        string_list_mock.assert_called_once_with(data)

    def test_should_return_path_list_when_giving_correct_input(self):
        assert [Path('/tmp/bar'), Path('/usr/bin/python')] == path_list('/tmp/bar:/usr/bin/python')
