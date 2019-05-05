"""Tests method load_from_toml"""
from pathlib import Path

import pytest

from configuror.exceptions import DecodeError


def test_method_return_false_when_a_single_file_is_unknown_and_ignore_flag_is_true(config):
    assert not config.load_from_toml('foo.txt', ignore_file_absence=True)


def test_method_raises_error_when_a_single_file_is_unknown_and_ignore_flag_is_false(config):
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_toml('foo.txt')

    assert 'file foo.txt not found on the filesystem' == str(exc_info.value)


def test_method_raises_error_when_a_file_in_the_list_is_unknown_and_ignore_flag_is_false(config, tempdir):
    foo_path = Path(tempdir) / 'foo.txt'
    bar_path = Path(tempdir) / 'bar.txt'
    foo_path.touch()
    bar_path.touch()
    unknown_file = 'foobar.txt'
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_toml([f'{foo_path}', unknown_file, f'{bar_path}'])

    assert f'file {unknown_file} not found on the filesystem' == str(exc_info.value)


def test_method_raises_error_when_none_of_the_files_are_valid_and_ignore_flag_is_true(config):
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_toml(['foo.txt', 'bar.txt'], ignore_file_absence=True)

    assert 'the list does not contain one toml valid file' == str(exc_info.value)


@pytest.mark.parametrize('filenames', [2, 2.5, {'foo': 'bar'}])
def test_method_raises_error_when_filenames_does_not_have_the_correct_type(config, filenames):
    with pytest.raises(TypeError) as exc_info:
        config.load_from_toml(filenames)

    assert 'filenames must represent a path or list of paths' == str(exc_info.value)


# this test avoids to check all cases already tested with method _filter_paths
@pytest.mark.parametrize('filenames', ['foo.txt', ['foo.txt']])
def test_method_calls_correctly_private_method_filter_paths(config, tempdir, mocker, filenames):
    filter_path_mock = mocker.patch('configuror.main.Config._filter_paths')
    expected_filenames = []
    if isinstance(filenames, str):
        p = Path(tempdir) / filenames
        p.touch()
        expected_filenames = [f'{p}']
    else:
        for filename in filenames:
            p = Path(tempdir) / filename
            p.touch()
            expected_filenames.append(f'{p}')
    with pytest.raises(TypeError):  # we don't want to worry about toml parsing error
        config.load_from_toml(expected_filenames)

    filter_path_mock.assert_called_once_with(expected_filenames, False)


def test_method_updates_config_when_passing_valid_toml_file(config):
    return_value = config.load_from_toml('dummy.toml')

    assert return_value is True
    for item in ['title', 'owner', 'database', 'servers', 'clients']:
        assert item in config
    assert 'TOML Example' == config['title']


def test_method_updates_config_when_passing_list_of_toml_files(config, tempdir):
    path = Path(tempdir) / 'test.ini'
    path.write_text('\n'.join(['foo=2', "bar='char'"]))
    return_value = config.load_from_toml(['dummy.toml', f'{path}'])

    assert return_value is True
    for item in ['title', 'owner', 'database', 'servers', 'clients', 'foo', 'bar']:
        assert item in config
    assert 'TOML Example' == config['title']
    assert 'char' == config['bar']
    assert 2 == config['foo']


def test_method_raises_error_when_a_single_file_is_not_toml_formatted(config):
    with pytest.raises(DecodeError) as exc_info:
        config.load_from_toml('dummy.yaml')

    assert 'one of your files is not well toml formatted' == str(exc_info.value)


def test_method_raises_error_when_a_file_in_the_list_is_not_when_toml_formatted(config):
    with pytest.raises(DecodeError) as exc_info:
        config.load_from_toml(['dummy.toml', 'dummy.yaml'])

    assert 'one of your files is not well toml formatted' == str(exc_info.value)
