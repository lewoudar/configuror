from pathlib import Path

import pytest

from configuror.exceptions import FileTypeError


class TestIsPathOK:
    """test method _path_is_ok"""

    def test_method_returns_true_when_file_exists(self, config, tempdir):
        file_path = Path(tempdir) / 'foo.txt'
        file_path.touch()

        assert config._path_is_ok(file_path)

    def test_method_returns_false_when_file_does_not_exist(self, config):
        assert not config._path_is_ok('foo', ignore_file_absence=True)

    def test_method_raises_error_when_ignore_flag_is_false(self, config):
        filename = 'foo'
        with pytest.raises(FileNotFoundError) as exc_info:
            config._path_is_ok(filename)

        assert f'file {filename} not found' == str(exc_info.value)


class TestCheckFileType:
    """test method _check_file_path"""

    @pytest.mark.parametrize(('filename', 'file_type'), [
        ('dummy.json', 'json'),
        ('dummy.yaml', 'yaml'),
        ('dummy.ini', 'ini'),
        ('dummy.toml', 'toml')
    ])
    def test_method_does_not_raise_error_when_giving_correct_file_and_type(self, config, filename, file_type):
        try:
            config._check_file_type(filename, file_type)
        except FileTypeError:
            pytest.fail(f'Unexpected fail with filename {filename} and file type "{file_type}"')

    @pytest.mark.parametrize(('original_filename', 'new_filename', 'file_type'), [
        ('dummy.yaml', 'dummy.yml', 'yaml'),
        ('dummy.ini', 'dummy.cfg', 'ini')
    ])
    def test_method_does_not_raise_error_with_some_suffix_aliases(self, config, tempdir, original_filename,
                                                                  new_filename, file_type):
        path = Path(tempdir) / original_filename
        path = path.with_name(new_filename)
        try:
            config._check_file_type(f'{path}', file_type)
        except FileTypeError:
            pytest.fail(f'Unexpected fail with filename {path} and file type "{file_type}"')

    @pytest.mark.parametrize(('filename', 'file_type'), [
        ('dummy.txt', 'yaml'),
        ('dummy', 'json'),
        ('dummy.php', 'ini')
    ])
    def test_method_raises_error_when_file_type_is_unknown(self, config, filename, file_type):
        with pytest.raises(FileTypeError) as exc_info:
            config._check_file_type(filename, file_type)

        assert f'{filename} is not a {file_type} file' == str(exc_info.value)
