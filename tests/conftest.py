import tempfile

import pytest

from configuror.main import Config


@pytest.fixture()
def config():
    return Config()


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir
