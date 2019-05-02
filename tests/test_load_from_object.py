class Foo:
    a = '2'
    b = 1
    A = ['a', 'b']
    FOO = 'bar'


class Bar:
    a = 2
    b = '1'


class TestLoadFromObject:
    def test_method_updates_config_attributes_when_passing_object_with_valid_attributes(self, config):
        foo = Foo()
        config.load_from_object(foo)

        assert {'A': ['a', 'b'], 'FOO': 'bar'} == config

    def test_config_object_is_empty_when_updating_with_object_having_lowercase_attributes(self, config):
        bar = Bar()
        config.load_from_object(bar)

        assert 0 == len(config)
