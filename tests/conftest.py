import tempfile
import os

import pytest

from configuror.main import Config


@pytest.fixture()
def config():
    """A Config instance to use in tests."""
    return Config()


@pytest.fixture()
def clean_env():
    """
    Removes some environment variables that may have been set by some tests
    working with dummy.env file.
    """
    for key in ['FOO', 'THOR', 'IRON', 'NAME', 'PERSONAL_DIR']:
        os.environ.pop(key, None)


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir
