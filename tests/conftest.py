import pytest

from configuror.main import Config


@pytest.fixture()
def config():
    return Config()
