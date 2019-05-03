"""Tests method Config.load_from_json"""
from pathlib import Path

import pytest

from configuror.exceptions import DecodeError


def test_method_return_false_when_file_is_unknown_and_ignore_flag_is_true(config):
    assert config.load_from_json('foo.txt', ignore_file_absence=True) is False


def test_method_raises_error_when_file_is_unknown_and_ignore_flag_is_false(config):
    with pytest.raises(FileNotFoundError):
        config.load_from_json('foo.txt')


def test_method_updates_config_when_passing_valid_json_file(config):
    return_value = config.load_from_json('dummy.json')

    assert return_value is True
    for item in ['title', 'owner', 'database', 'servers', 'clients']:
        assert item in config
    assert 'JSON Example' == config['title']


@pytest.mark.parametrize('filename', ['foo.txt', 'foo.json'])
def test_method_raises_error_when_file_content_is_not_valid(config, tempdir, filename):
    path = Path(tempdir) / filename
    path.write_text('hello world!')

    with pytest.raises(DecodeError) as exc_info:
        config.load_from_json(f'{path}')

    assert f'{path} is not well json formatted' == str(exc_info.value)
