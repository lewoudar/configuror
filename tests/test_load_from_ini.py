"""Tests method load_from_ini"""
import pytest

from configuror.exceptions import DecodeError


def test_method_return_false_when_a_single_file_is_unknown_and_ignore_flag_is_true(config):
    assert not config.load_from_ini('foo.txt', ignore_file_absence=True)


def test_method_raises_error_when_a_single_file_is_unknown_and_ignore_flag_is_false(config):
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_ini('foo.txt')

    assert 'file foo.txt not found on the filesystem' == str(exc_info.value)


@pytest.mark.parametrize('filenames', [2, 2.5, {'foo': 'bar'}])
def test_method_raises_error_when_filenames_does_not_have_the_correct_type(config, filenames):
    with pytest.raises(TypeError) as exc_info:
        config.load_from_ini(filenames)

    assert 'filenames must represent a path or list of paths' == str(exc_info.value)


def test_method_raises_error_when_a_file_in_the_list_is_unknown_and_ignore_flag_is_false(config, tmp_path):
    foo_path = tmp_path / 'foo.txt'
    bar_path = tmp_path / 'bar.txt'
    foo_path.touch()
    bar_path.touch()
    unknown_file = 'foobar.txt'
    with pytest.raises(FileNotFoundError) as exc_info:
        config.load_from_ini([f'{foo_path}', unknown_file, f'{bar_path}'])

    assert f'file {unknown_file} not found on the filesystem' == str(exc_info.value)


def test_config_has_a_default_entry_when_none_of_the_files_are_valid_and_ignore_flag_is_true(config):
    config.load_from_ini(['foo.txt', 'bar.txt'], ignore_file_absence=True)

    assert 1 == len(config)
    assert {} == config['DEFAULT']


# this test avoids to check all cases already tested with method _filter_paths
@pytest.mark.parametrize('filenames', ['foo.txt', ['foo.txt']])
def test_method_calls_correctly_private_method_filter_paths(tmp_path, config, mocker, filenames):
    filter_path_mock = mocker.patch('configuror.main.Config._filter_paths')
    expected_filenames = []
    if isinstance(filenames, str):
        p = tmp_path / filenames
        p.touch()
        expected_filenames = [f'{p}']
    else:
        for filename in filenames:
            p = tmp_path / filename
            p.touch()
            expected_filenames.append(f'{p}')

    config.load_from_ini(expected_filenames)

    filter_path_mock.assert_called_once_with(expected_filenames, False)


@pytest.mark.parametrize('interpolation_method', [2, 2.5, ['a', 'b']])
def test_method_raises_error_when_interpolation_method_is_not_a_string(config, interpolation_method):
    with pytest.raises(TypeError) as exc_info:
        config.load_from_ini('foo.txt', interpolation_method=interpolation_method)

    assert 'interpolation_method must be either "basic" or "extended"' == str(exc_info.value)


@pytest.mark.parametrize('interpolation_method', ['extend', 'bas'])
def test_method_raises_error_when_interpolation_method_value_is_not_valid(config, interpolation_method):
    with pytest.raises(ValueError) as exc_info:
        config.load_from_ini('foo.txt', interpolation_method=interpolation_method)

    assert 'interpolation_method must be either "basic" or "extended"' == str(exc_info.value)


@pytest.mark.parametrize('interpolation_method', [
    'basic',
    'extended',
    'BASIC',
    'Extended',
    'BaSic',
    'exteNded'
])
def test_method_does_not_raise_error_when_interpolation_method_is_correct(tmp_path, config, interpolation_method):
    path = tmp_path / 'foo.txt'
    path.touch()
    try:
        config.load_from_ini(f'{path}', interpolation_method=interpolation_method)
    except ValueError:
        pytest.fail(f'Unexpected value error with interpolation_method = {interpolation_method}')


def test_method_updates_config_when_passing_a_valid_ini_file(config):
    return_value = config.load_from_ini('dummy.ini')

    assert return_value is True
    for item in ['databases', 'servers.alpha', 'servers.beta']:
        assert item in config
    assert '192.168.1.1' == config['databases']['server']


def test_method_updates_config_when_passing_list_of_ini_files_with_basic_interpolation(tmp_path, config):
    test_content_lines = [
        '[Paths]',
        'home_dir: /Users',
        'my_dir: %(home_dir)s/kevin'
    ]
    path = tmp_path / 'test.ini'
    path.write_text('\n'.join(test_content_lines))
    return_value = config.load_from_ini(['dummy.ini', f'{path}'])

    assert return_value is True
    for item in ['databases', 'servers.alpha', 'servers.beta', 'Paths']:
        assert item in config
    assert '192.168.1.1' == config['databases']['server']
    assert '/Users/kevin' == config['Paths']['my_dir']


def test_method_updates_config_when_passing_list_of_ini_files_with_extended_interpolation(tmp_path, config):
    test_content_lines = [
        '[Paths]',
        'home_dir: /Users',
        'my_dir: ${home_dir}/kevin',
        'system_dir: /System',
        '[Frameworks]',
        'path: ${Paths:system_dir}/Library/Frameworks/'
    ]
    path = tmp_path / 'test.ini'
    path.write_text('\n'.join(test_content_lines))
    return_value = config.load_from_ini(['dummy.ini', f'{path}'], interpolation_method='extended')

    assert return_value is True
    for item in ['databases', 'servers.alpha', 'servers.beta', 'Paths', 'Frameworks']:
        assert item in config
    assert '192.168.1.1' == config['databases']['server']
    assert '/Users/kevin' == config['Paths']['my_dir']
    assert '/System/Library/Frameworks/' == config['Frameworks']['path']


def test_method_raises_error_when_a_single_file_is_not_ini_formatted(config):
    with pytest.raises(DecodeError) as exc_info:
        config.load_from_ini('dummy.yaml')

    assert f'one of your files is not well ini formatted' == str(exc_info.value)


def test_method_raises_error_when_a_file_in_the_list_is_not_ini_formatted(config):
    with pytest.raises(DecodeError) as exc_info:
        config.load_from_ini(['dummy.ini', 'dummy.yaml'])

    assert f'one of your files is not well ini formatted' == str(exc_info.value)
