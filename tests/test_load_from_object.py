import pytest


class Foo:
    a = '2'
    b = 1
    A = ['a', 'b']
    FOO = 'bar'


class Bar:
    a = 2
    b = '1'


class TestLoadFromObject:
    def test_method_updates_config_when_passing_object_with_valid_attributes(self, config):
        foo = Foo()
        config.load_from_object(foo)

        assert {'A': ['a', 'b'], 'FOO': 'bar'} == config

    def test_config_is_empty_when_updating_with_object_having_lowercase_attributes(self, config):
        bar = Bar()
        config.load_from_object(bar)

        assert 0 == len(config)

    def test_method_updates_config_when_passing_module_path(self, config):
        config.load_from_object('tests.dummy_module')

        assert 'foo' == config['A']
        assert 'b' not in config

    def test_method_raises_error_when_module_not_found(self, config):
        with pytest.raises(ModuleNotFoundError):
            config.load_from_object('foo.bar')
