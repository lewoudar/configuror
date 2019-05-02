"""Test all environment related actions"""


class TestGetEnv:
    def test_getenv_returns_correct_info_when_env_exists(self, monkeypatch, config):
        monkeypatch.setenv('foo', 'bar')
        assert 'bar' == config.getenv('foo')

    def test_getenv_returns_none_when_env_does_not_exist(self, config):
        assert config.getenv('foo') is None
