# -*- coding: utf-8 -*-
"""Phantom test cases."""
import pytest

from yapam.phantom import PhantomAmmo


pytestmark = [pytest.mark.phantom]


@pytest.fixture
def phantom_ammo_dict(logger):
    """Fixture with PhantomAmmo parameters without body."""
    ammo_dict = {
        'host': '127.0.0.1',
        'port': 8888,
        'url': '/auth',
        'method': 'GET',
        'log': logger,
        'case': 'tests',
        'extra_headers': {'Authorization': 'token'},
        'body': ''
    }
    return ammo_dict


@pytest.fixture
def phantom_ammo_with_body_dict(phantom_ammo_dict):
    """Fixture with PhantomAmmo parameters with body."""
    ammo_dict = phantom_ammo_dict
    ammo_dict['method'] = 'POST'
    ammo_dict['body'] = '{\"username\": \"admin\", \"password\": \"admin\"}'
    ammo_dict['log'] = None
    return ammo_dict


@pytest.fixture
def phantom_headers_str():
    """Fixture with expected default headers converted to str."""
    headers_str = ('Authorization: token\r\n'
                   'Host: 127.0.0.1:8888\r\n'
                   'User-Agent: phantom\r\n'
                   'Accept: */*\r\n'
                   'Content-Type: application/json\r\n'
                   'Connection: Close'
                   )
    return headers_str


@pytest.fixture
def phantom_headers_with_body_str(phantom_headers_str):
    """Fixture with expected default headers for request with body converted to str."""
    return '\r\n'.join([phantom_headers_str, 'Content-Length: 42'])


@pytest.fixture
def phantom_request_str(phantom_headers_str):
    """Fixture with expected Phantom request str."""
    request_str = 'GET /auth HTTP/1.1\r\n' + phantom_headers_str
    return request_str


@pytest.fixture
def phantom_request_with_body_str(phantom_headers_with_body_str):
    """Fixture with expected Phantom request with body str."""
    return '\r\n'.join(
        ['POST /auth HTTP/1.1', phantom_headers_with_body_str, '\r\n{"username": "admin", "password": "admin"}'])


@pytest.fixture
def phantom_bullet_str(phantom_request_str):
    """Fixture with expected phantom bullet."""
    return '147 tests\n' + phantom_request_str + '\r\n\r\n'


@pytest.fixture
def phantom_bullet_with_body_str(phantom_request_with_body_str):
    """Fixture with expected phantom bullet for request with body."""
    return '214 tests\n' + phantom_request_with_body_str + '\r\n\r\n'


@pytest.fixture
def phantom_ammo_inst(phantom_ammo_dict):
    """Fixture with PhantomAmmo (without body) instance."""
    return PhantomAmmo(**phantom_ammo_dict)


@pytest.fixture
def phantom_ammo_with_body_inst(phantom_ammo_with_body_dict):
    """Fixture with PhantomAmmo (with body) instance."""
    return PhantomAmmo(**phantom_ammo_with_body_dict)


class TestPhantomAmmo:
    """Phantom ammo without body test cases."""

    def test_init(self, phantom_ammo_dict):
        """Constructor test."""
        assert isinstance(PhantomAmmo(**phantom_ammo_dict), PhantomAmmo)

    def test_headers_property(self, phantom_ammo_inst, phantom_headers_str):
        """Check that headers property converted as expected."""
        assert phantom_ammo_inst.headers == phantom_headers_str

    def test_request_property(self, phantom_ammo_inst, phantom_request_str):
        """Check that request property converted as expected."""
        assert phantom_ammo_inst.request == phantom_request_str

    def test_bullet_property(self, phantom_ammo_inst, phantom_bullet_str, temporary_log_file):
        """Check that bullet property converted as expected."""
        assert phantom_ammo_inst.bullet == phantom_bullet_str

        def last_log_line(file_name: str):
            """Return last string from temporary log."""
            with open(file_name, 'r') as log_file:
                lines = log_file.readlines()
            return lines[-1]
        for attr in phantom_bullet_str.split('\n'):
            assert attr.replace('\r', '') in last_log_line(temporary_log_file)


class TestPhantomAmmoWithBody:
    """Phantom ammo with body test cases."""

    def test_init(self, phantom_ammo_with_body_dict):
        """Constructor test."""
        assert isinstance(PhantomAmmo(**phantom_ammo_with_body_dict), PhantomAmmo)

    def test_headers_property(self, phantom_ammo_with_body_inst, phantom_headers_str):
        """Check that headers property converted as expected."""
        assert phantom_ammo_with_body_inst.headers == phantom_headers_str

    def test_request_property(self, phantom_ammo_with_body_inst, phantom_request_with_body_str):
        """Check that request property converted as expected."""
        assert phantom_ammo_with_body_inst.request == phantom_request_with_body_str

    def test_bullet_property(self, phantom_ammo_with_body_inst, phantom_bullet_with_body_str):
        """Check that bullet property converted as expected."""
        assert phantom_ammo_with_body_inst.bullet == phantom_bullet_with_body_str
