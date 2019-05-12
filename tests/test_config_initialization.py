import pytest

from configuror.main import Config


@pytest.mark.parametrize('defaults', [
    {},
    {'a': 1, 'b': 'c', 'foo': ['bar']},
    {'a': {'b': 'c'}, 'd': 4.5}
])
def test_config_loads_default_config_variables_passed_at_init_time(defaults):
    config = Config(**defaults)
    assert defaults == config


def test_config_calls_methods_for_adding_files(mocker):
    add_mapping_files_mock = mocker.patch('configuror.main.Config.load_from_mapping_files')
    add_files_mock = mocker.patch('configuror.main.Config.load_from_files')

    mapping_files = {'ini': ['dummy.ini'], 'toml': ['dummy.toml']}
    files = ['dummy.env', 'dummy_module.py']
    Config(mapping_files=mapping_files, files=files, ignore_file_absence=True)

    add_mapping_files_mock.assert_called_once_with(mapping_files, True)
    add_files_mock.assert_called_once_with(files, True)
