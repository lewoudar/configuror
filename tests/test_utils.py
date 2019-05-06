"""Tests util module"""
from configparser import ConfigParser

import pytest

from configuror.utils import convert_ini_config_to_dict


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
