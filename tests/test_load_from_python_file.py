from pathlib import Path

import pytest

from configuror.exceptions import FileTypeError


def test_method_returns_false_when_file_is_unknown_and_ignore_flag_is_true(config):
    assert not config.load_from_python_file('foo.txt', ignore_file_absence=True)


def test_method_raises_error_when_file_is_unknown_and_ignore_flag_is_false(config):
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_python_file('foo.txt')

    assert 'file foo.txt not found' == str(exc_info.value)


@pytest.mark.parametrize('filename', [2, 2.5, ['a', 'b']])
def test_method_raises_error_when_filename_is_not_a_string(config, filename):
    with pytest.raises(TypeError) as exc_info:
        config.load_from_python_file(filename)

    assert f'{filename} is not a string representing a path' == str(exc_info.value)


def test_method_updates_config_when_passing_valid_python_file(config, tempdir):
    content_lines = ['A = "foo"', 'B = "bar"', 'c = "char"']
    path = Path(tempdir) / 'test.py'
    path.write_text('\n'.join(content_lines))
    return_value = config.load_from_python_file(f'{path}')

    assert return_value is True
    assert 'foo' == config['A']
    assert 'bar' == config['B']
    assert 'c' not in config


def test_method_raises_error_when_filename_is_not_a_valid_python_file(config, tempdir):
    path = Path(tempdir) / 'foo.txt'
    path.write_text('hello world!')

    with pytest.raises(FileTypeError) as exc_info:
        config.load_from_python_file(f'{path}')

    assert f'{path} is not a python file' == str(exc_info.value)
