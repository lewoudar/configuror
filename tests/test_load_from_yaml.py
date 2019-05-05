"""Tests method load_from_yaml"""
from pathlib import Path

import pytest
import yaml

from configuror.exceptions import DecodeError


def test_method_return_false_when_file_is_unknown_and_ignore_flag_is_true(config):
    config.load_from_yaml('foo.txt', ignore_file_absence=True)


def test_method_raises_error_when_file_is_unknown_and_ignore_flag_is_false(config):
    with pytest.raises(FileNotFoundError):
        config.load_from_yaml('foo.txt')


def test_method_updates_config_when_passing_valid_yaml_file(config):
    return_value = config.load_from_yaml('dummy.yaml')

    assert return_value is True
    for item in ['title', 'owner', 'database', 'servers', 'clients']:
        assert item in config
    assert 'YAML Example' == config['title']


@pytest.mark.parametrize('data', [2, 'hello', [1, 'foo']])
def test_method_returns_false_when_loaded_data_is_not_a_dict(config, tempdir, data):
    path = Path(tempdir) / 'test.yml'
    with path.open(mode='w') as f:
        yaml.dump(data, f)

    assert not config.load_from_yaml(f'{path}')
    assert {} == config


@pytest.mark.parametrize('filename', ['foo.txt', 'foo.yaml'])
def test_method_raises_error_when_file_content_is_not_valid(config, tempdir, filename):
    content_lines = ['[section]', 'foo=bar']
    path = Path(tempdir) / filename
    path.write_text('\n'.join(content_lines))

    with pytest.raises(DecodeError) as exc_info:
        config.load_from_yaml(f'{path}')

    assert f'{path} is not well yaml formatted' == str(exc_info.value)
