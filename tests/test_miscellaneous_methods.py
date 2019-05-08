"""Test all config methods which doesn't fit in other test modules"""
import os

import pytest

from configuror.exceptions import UnknownExtensionError


@pytest.fixture()
def mapping():
    return {
        'IMAGE_STORE_TYPE': 'fs',
        'IMAGE_STORE_PATH': '/var/app/images',
        'IMAGE_STORE_BASE_URL': 'http://img.website.com',
        'WORKERS': 2,
        4: 'foo'
    }


class TestGetDictFromNamespace:
    """tests method get_dict_from_namespace"""

    @pytest.mark.parametrize(('expected_result', 'lowercase', 'trim_namespace'), [
        (
                {
                    'type': 'fs',
                    'path': '/var/app/images',
                    'base_url': 'http://img.website.com'
                }, True, True
        ),
        (
                {
                    'TYPE': 'fs',
                    'PATH': '/var/app/images',
                    'BASE_URL': 'http://img.website.com'
                }, False, True
        ),
        (
                {
                    'image_store_type': 'fs',
                    'image_store_path': '/var/app/images',
                    'image_store_base_url': 'http://img.website.com'
                }, True, False
        ),
        (
                {
                    'IMAGE_STORE_TYPE': 'fs',
                    'IMAGE_STORE_PATH': '/var/app/images',
                    'IMAGE_STORE_BASE_URL': 'http://img.website.com'
                }, False, False
        )
    ])
    def test_method_return_correct_dict_with_lowercase_and_trim_namespace(self, config, mapping, expected_result,
                                                                          lowercase, trim_namespace):
        config.update(mapping)
        previous_config = dict(config)

        assert expected_result == config.get_dict_from_namespace('IMAGE_STORE_', lowercase, trim_namespace)
        assert previous_config == config


class TestAddMappingFiles:
    """Tests method add_mapping_files"""

    def test_method_returns_false_when_dict_is_none(self, config):
        assert not config.add_mapping_files()

    def test_method_returns_false_when_files_are_empty(self, config):
        mapping_files = {
            'env': ['.env'],
            'ini': ['foo.toml']
        }
        assert not config.add_mapping_files(mapping_files, ignore_file_absence=True)

    @pytest.mark.parametrize('unknown_extension', ['bat', 'ps1'])
    def test_method_raises_error_when_extension_is_unknown(self, config, unknown_extension):
        with pytest.raises(UnknownExtensionError) as exc_info:
            config.add_mapping_files({unknown_extension: []})

        assert f'extension "{unknown_extension}" is not supported' == str(exc_info.value)

    @pytest.mark.parametrize('files', [2, 2.5, {'a': 'b'}])
    def test_method_raises_error_if_a_mapping_value_is_not_a_list(self, config, files):
        with pytest.raises(TypeError) as exc_info:
            config.add_mapping_files({'env': files})

        assert f'{files} is not a list of files' == str(exc_info.value)

    @pytest.mark.parametrize('extension', ['PYTHON', 'env', 'Ini'])
    def test_method_does_not_raise_error_with_supported_extensions(self, config, extension):
        try:
            config.add_mapping_files({extension: []})
        except UnknownExtensionError:
            pytest.fail(f'Unexpected fail with extension {extension}')

    # I deliberately avoided testing ini and toml methods because they call internally path_files
    def test_method_calls_filter_paths_intern_method(self, config, mocker):
        mapping_files = {
            'env': [],
            'python': ['dummy.python'],
            'yaml': []
        }
        filter_paths_mock = mocker.patch('configuror.main.Config._filter_paths')
        filter_paths_mock.return_value = []
        config.add_mapping_files(mapping_files, ignore_file_absence=True)

        assert 3 == len(filter_paths_mock.mock_calls)
        filter_paths_mock.assert_any_call(['dummy.python'], True)
        filter_paths_mock.assert_any_call([], True)

    def test_method_calls_different_loading_methods(self, config, mocker):
        mapping_files = {
            'env': ['dummy.env'],
            'python': ['dummy_module.py'],
            'toml': ['dummy.toml'],
            'ini': ['dummy.ini'],
            'yaml': ['dummy.yaml'],
            'json': ['dummy.json']
        }
        load_from_json_mock = mocker.patch('configuror.main.Config.load_from_json')
        load_from_toml_mock = mocker.patch('configuror.main.Config.load_from_toml')
        load_from_ini_mock = mocker.patch('configuror.main.Config.load_from_ini')
        load_from_yaml_mock = mocker.patch('configuror.main.Config.load_from_yaml')
        load_from_python_mock = mocker.patch('configuror.main.Config.load_from_python_file')
        load_from_dotenv_mock = mocker.patch('configuror.main.Config.load_from_dotenv')

        config.add_mapping_files(mapping_files)

        load_from_json_mock.assert_called_once_with('dummy.json')
        load_from_toml_mock.assert_called_once_with(['dummy.toml'])
        load_from_ini_mock.assert_called_once_with(['dummy.ini'])
        load_from_yaml_mock.assert_called_once_with('dummy.yaml')
        load_from_python_mock.assert_called_once_with('dummy_module.py')
        load_from_dotenv_mock.assert_called_once_with('dummy.env')

    @pytest.mark.usefixtures('clean_env')
    def test_method_updates_correctly_config(self, config):
        mapping_files = {
            'env': ['dummy.env'],
            'ini': ['foo.ini'],  # unknown file deliberately added
            'python': ['dummy_module.py'],
            'toml': ['dummy.toml'],
        }
        return_value = config.add_mapping_files(mapping_files, ignore_file_absence=True)

        assert return_value is True
        assert 'foo' == config['A']
        assert '/home/Kevin T' == config['PERSONAL_DIR'] == os.environ['PERSONAL_DIR']
        assert 'TOML Example' == config['title']
