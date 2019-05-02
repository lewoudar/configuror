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
