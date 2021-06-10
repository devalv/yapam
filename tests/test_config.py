# -*- coding: utf-8 -*-
"""Config test cases."""
import json

import pytest

from yapam.config import AmmoConfig, ConfigRequest


pytestmark = [pytest.mark.config]


@pytest.fixture
def bad_config_request():
    """Parameters missing in the ConfigRequest."""
    request_dict = {
        'host': '127.0.0.1',
        'port': 8888,
        'url': '/auth',
        'method': 'POST',
        'body': {'username': 'admin', 'password': 'admin'},
        'headers': 'headers'
    }
    return request_dict


@pytest.fixture(scope='session')
def good_config_file(tmpdir_factory):
    """Temporary config file."""
    fn = str(tmpdir_factory.mktemp('data').join('data.json'))
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(AmmoConfig().template_blueprint, f, ensure_ascii=False, indent=4)
    return fn


@pytest.fixture(scope='session')
def bad_config_file(tmpdir_factory):
    """Temporary bad config file."""
    fn = str(tmpdir_factory.mktemp('data').join('data.json'))
    data = AmmoConfig().template_blueprint
    # add bad parameter
    data['REQUESTS'] = [
        {
            'host': '127.0.0.1',
            'port': '8888',
            'url': '/auth',
            'method': 'BAD',
        }]
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return fn


@pytest.mark.request
class TestConfigRequest:
    """ConfigRequest test cases."""

    def test_good_request(self, config_request):
        """Check that expected request structure allowed."""
        request_instance = ConfigRequest(**config_request)
        assert isinstance(request_instance, ConfigRequest)

    def test_bad_request(self, bad_config_request):
        """Check that unexpected request structure not allowed."""
        try:
            ConfigRequest(**bad_config_request)
        except TypeError:
            assert True
        else:
            raise AssertionError()


class TestAmmoConfig:
    """AmmoConfig test cases."""

    def test_good_config_load(self, good_config_file):
        """Check that allowed structure of config file can be parsed."""
        cfg = AmmoConfig(good_config_file)
        assert cfg.requests

    def test_bad_config_load(self, bad_config_file):
        """Check that not allowed structure of config file can not be parsed."""
        try:
            AmmoConfig(bad_config_file)
        except TypeError as err:
            assert 'bad parameters' in str(err)
        else:
            raise AssertionError()

    def test_create_template(self, temporary_json_file):
        """Check that template with config blueprint can be created."""
        AmmoConfig().create_template(temporary_json_file)
        assert True
