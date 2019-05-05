from pathlib import Path

import pytest

from configuror.exceptions import FileTypeError


class TestPathIsOK:
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

        assert f'file {filename} not found on the filesystem' == str(exc_info.value)


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


class TestFilterPaths:
    def test_method_returns_correct_filtered_list_when_flag_option_is_true(self, config, tempdir):
        existing_paths = []
        for filename in ['foo.txt', 'bar.txt']:
            p = Path(tempdir) / filename
            p.touch()
            existing_paths.append(p)

        existing_paths = [f'{path}' for path in existing_paths]
        paths = [*existing_paths, f'{Path(tempdir) / "foobar.txt"}']

        assert existing_paths == config._filter_paths(paths, ignore_file_absence=True)

    @pytest.mark.parametrize('filenames', [[], ['foo.txt', 'bar.txt']])
    def test_method_returns_empty_list_when_no_file_exists_on_the_system(self, config, filenames):
        assert [] == config._filter_paths(filenames, ignore_file_absence=True)

    def test_method_raises_error_when_a_file_is_unknown_in_a_list_with_flag_option_false(self, config, tempdir):
        existing_paths = []
        for filename in ['foo.txt', 'bar.txt']:
            p = Path(tempdir) / filename
            p.touch()
            existing_paths.append(p)

        existing_paths = [f'{path}' for path in existing_paths]
        missing_path = Path(tempdir) / 'foobar.txt'
        paths = [*existing_paths, f'{missing_path}']

        with pytest.raises(FileNotFoundError) as exc_info:
            config._filter_paths(paths)

        assert f'file {missing_path} not found on the filesystem' == str(exc_info.value)

    @pytest.mark.parametrize('ignore_absence', [True, False])
    def test_method_raises_error_when_element_in_the_list_is_not_a_string(self, config, tempdir, ignore_absence):
        path = Path(tempdir) / 'foo.txt'
        with pytest.raises(TypeError) as exc_info:
            config._filter_paths([f'{path}', 2], ignore_file_absence=ignore_absence)

        assert '2 is not a string representing a path' == str(exc_info.value)
