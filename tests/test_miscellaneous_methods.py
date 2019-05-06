"""Test all config methods which doesn't fit in other test modules"""
import pytest


@pytest.fixture()
def mapping():
    return {
        'IMAGE_STORE_TYPE': 'fs',
        'IMAGE_STORE_PATH': '/var/app/images',
        'IMAGE_STORE_BASE_URL': 'http://img.website.com',
        'WORKERS': 2,
        4: 'foo'
    }


class TestGetDictFromNamespace:
    """tests method get_dict_from_namespace"""

    @pytest.mark.parametrize(('expected_result', 'lowercase', 'trim_namespace'), [
        (
            {
                'type': 'fs',
                'path': '/var/app/images',
                'base_url': 'http://img.website.com'
            }, True, True
        ),
        (
            {
                'TYPE': 'fs',
                'PATH': '/var/app/images',
                'BASE_URL': 'http://img.website.com'
            }, False, True
        ),
        (
            {
                'image_store_type': 'fs',
                'image_store_path': '/var/app/images',
                'image_store_base_url': 'http://img.website.com'
            }, True, False
        ),
        (
            {
                'IMAGE_STORE_TYPE': 'fs',
                'IMAGE_STORE_PATH': '/var/app/images',
                'IMAGE_STORE_BASE_URL': 'http://img.website.com'
            }, False, False
        )
    ])
    def test_method_return_correct_dict_with_lowercase_and_trim_namespace(self, config, mapping, expected_result,
                                                                          lowercase, trim_namespace):
        config.update(mapping)
        previous_config = dict(config)

        assert expected_result == config.get_dict_from_namespace('IMAGE_STORE_', lowercase, trim_namespace)
        assert previous_config == config
