"""Test all environment related actions"""
import os

import pytest


class TestGetEnv:
    """Tests method getenv"""

    def test_getenv_returns_correct_info_when_env_exists(self, monkeypatch, config):
        monkeypatch.setenv('foo', 'bar')
        assert 'bar' == config.getenv('foo')

    def test_getenv_returns_none_when_env_does_not_exist(self, config):
        assert config.getenv('foo') is None


class TestLoadFromDotEnv:
    """tests method load_from_dotenv"""

    def test_method_return_false_when_file_is_unknown_and_ignore_flag_is_true(self, config):
        assert not config.load_from_dotenv('foo.txt', ignore_file_absence=True)

    def test_method_raises_error_when_file_is_unknown_and_ignore_flag_is_false(self, config):
        with pytest.raises(FileNotFoundError):
            config.load_from_dotenv('foo.txt')

    @pytest.mark.parametrize('lines', [
        [''],
        ['# comment 1', '  ', '# comment 2']
    ])
    def test_method_return_false_when_extracted_data_is_empty(self, tmp_path, config, lines):
        path = tmp_path / '.env'
        path.write_text('\n'.join(lines))

        assert not config.load_from_dotenv(path)

    @pytest.mark.usefixtures('clean_env')
    def test_method_set_config_and_environment_when_giving_a_correct_file(self, config):
        keys = ['FOO', 'THOR', 'IRON', 'NAME', 'PERSONAL_DIR']
        return_value = config.load_from_dotenv('dummy.env')

        assert return_value is True
        for key in keys:
            assert key in config
            assert key in os.environ

        assert 'RAGNAROK' == config['THOR'] == os.environ['THOR']
        assert 'Kevin T' == config['NAME'] == os.environ['NAME']
        assert '/home/Kevin T' == config['PERSONAL_DIR'] == os.environ['PERSONAL_DIR']
