# -*- coding: utf-8 -*-
"""Phantom test cases."""
import pytest

from yapam.phantom import PhantomAmmo


pytestmark = [pytest.mark.phantom]


def convert_headers_str_to_dict(headers_str: str) -> dict:
    """Convert headers in str format to dict."""
    headers_gen = (header.split(': ') for header in headers_str.split('\r\n'))
    headers_dict = {header[0]: header[1] for header in headers_gen}
    return headers_dict


@pytest.fixture
def phantom_ammo_dict(logger):
    """Phantom ammo parameters without body."""
    ammo_dict = {
        'host': '127.0.0.1',
        'port': 8888,
        'url': '/auth',
        'method': 'GET',
        'log': logger,
        'case': 'tests',
        'extra_headers': {'Authorization': 'token'},
        'body': {}
    }
    return ammo_dict


@pytest.fixture
def phantom_ammo_with_body_dict(phantom_ammo_dict):
    """Phantom ammo parameters with body."""
    ammo_dict = phantom_ammo_dict
    ammo_dict['method'] = 'POST'
    ammo_dict['body'] = {'username': 'admin', 'password': 'admin'}
    ammo_dict['log'] = None
    return ammo_dict


@pytest.fixture
def phantom_headers_dict():
    """Phantom default headers as a dictionary."""
    headers_dict = {
        'Authorization': 'token',
        'Host': '127.0.0.1:8888',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Connection': 'Close',
        'User-Agent': 'phantom'
    }
    return headers_dict


@pytest.fixture
def phantom_headers_with_body_dict(phantom_headers_dict):
    """Phantom default headers with additional parameter as a dict."""
    headers_dict = {'Content-Length': '42'}
    headers_dict.update(phantom_headers_dict)
    return headers_dict


@pytest.fixture
def phantom_request_dict(phantom_headers_dict):
    """Phantom request parameter as a strange dict."""
    body_dict = dict()
    body_dict['1'] = 'GET /auth HTTP/1.1'
    body_dict['2'] = phantom_headers_dict
    return body_dict


@pytest.fixture
def phantom_request_with_body_dict(phantom_headers_with_body_dict):
    """Phantom request as a strange dictionary."""
    body_dict = dict()
    body_dict['1'] = 'POST /auth HTTP/1.1'
    body_dict['2'] = phantom_headers_with_body_dict
    body_dict['3'] = '{"username": "admin", "password": "admin"}'
    return body_dict


@pytest.fixture
def phantom_bullet_dict(phantom_request_dict):
    """Phantom bullet property values as a dictionary."""
    bullet_dict = {'0': '147 tests'}
    bullet_dict.update(phantom_request_dict)
    return bullet_dict


@pytest.fixture
def phantom_bullet_with_body_dict(phantom_request_with_body_dict):
    """Phantom bullet with body property values as a dictionary."""
    bullet_with_body_dict = {'0': '214 tests'}
    bullet_with_body_dict.update(phantom_request_with_body_dict)
    return bullet_with_body_dict


@pytest.fixture
def phantom_ammo_inst(phantom_ammo_dict):
    """Phantom ammo (without body) instance."""
    return PhantomAmmo(**phantom_ammo_dict)


@pytest.fixture
def phantom_ammo_with_body_inst(phantom_ammo_with_body_dict):
    """Phantom ammo (with body) instance."""
    return PhantomAmmo(**phantom_ammo_with_body_dict)


class TestPhantomAmmo:
    """Phantom ammo without body test cases."""

    @staticmethod
    def convert_request_str_to_dict(request_str: str) -> dict:
        """Convert request in str format to dict."""
        str_list = [el for el in request_str.split('\r\n') if el]
        request_dict = dict()
        request_dict['1'] = str_list[0]
        request_dict['2'] = convert_headers_str_to_dict(
            '\r\n'.join(str_list[1:]))
        return request_dict

    @staticmethod
    def convert_bullet_str_to_dict(bullet_str: str) -> dict:
        """Convert request in str format to dict."""
        str_list = [el for el in bullet_str.replace('\r', '').split('\n') if el]
        bullet_dict = dict()
        bullet_dict['0'] = str_list[0]
        bullet_dict['1'] = str_list[1]
        bullet_dict['2'] = convert_headers_str_to_dict(
            '\r\n'.join([header_str for header_str in str_list[2:] if header_str]))
        return bullet_dict

    def test_init(self, phantom_ammo_dict):
        """Constructor test."""
        assert isinstance(PhantomAmmo(**phantom_ammo_dict), PhantomAmmo)

    def test_headers_property(self, phantom_ammo_inst, phantom_headers_dict):
        """Check that headers property converted as expected."""
        assert convert_headers_str_to_dict(phantom_ammo_inst.headers) == phantom_headers_dict

    def test_request_property(self,
                              phantom_ammo_inst,
                              phantom_request_dict):
        """Check that request property converted as expected."""
        assert self.convert_request_str_to_dict(phantom_ammo_inst.request) == phantom_request_dict

    def test_bullet_property(self,
                             phantom_ammo_inst,
                             phantom_bullet_dict,
                             temporary_log_file):
        """Check that bullet property converted as expected."""
        assert self.convert_bullet_str_to_dict(phantom_ammo_inst.bullet) == phantom_bullet_dict

        def last_log_line(file_name: str):
            """Return last string from temporary log."""
            with open(file_name, 'r') as log_file:
                lines = log_file.readlines()
            return lines[-1]

        for val in phantom_bullet_dict.values():
            if isinstance(val, str):
                assert val in last_log_line(temporary_log_file)
            elif isinstance(val, dict):
                for k, v in val.items():
                    assert k in last_log_line(temporary_log_file)
                    assert v in last_log_line(temporary_log_file)


class TestPhantomAmmoWithBody:
    """Phantom ammo with body test cases."""

    @staticmethod
    def convert_request_with_body_to_dict(request_str: str) -> dict:
        """Convert request in str format to a dict."""
        str_list = [el for el in request_str.split('\r\n') if el]
        request_dict = dict()
        request_dict['1'] = str_list[0]
        request_dict['2'] = convert_headers_str_to_dict(
            '\r\n'.join(str_list[1:-1]))
        request_dict['3'] = str_list[-1]
        return request_dict

    @staticmethod
    def convert_bullet_with_body_to_dict(bullet_str: str) -> dict:
        """Convert request in str format to a dict."""
        str_list = [el for el in bullet_str.replace('\r', '').split('\n') if el]
        bullet_dict = dict()
        bullet_dict['0'] = str_list[0]
        bullet_dict['1'] = str_list[1]
        bullet_dict['2'] = convert_headers_str_to_dict(
            '\r\n'.join([header_str for header_str in str_list[2:-1] if header_str]))
        bullet_dict['3'] = str_list[-1]
        return bullet_dict

    def test_init(self, phantom_ammo_with_body_dict):
        """Constructor test."""
        assert isinstance(PhantomAmmo(**phantom_ammo_with_body_dict), PhantomAmmo)

    def test_headers_property(self, phantom_ammo_with_body_inst, phantom_headers_dict):
        """Check that headers property converted as expected."""
        assert convert_headers_str_to_dict(phantom_ammo_with_body_inst.headers) == phantom_headers_dict

    def test_request_property(self, phantom_ammo_with_body_inst, phantom_request_with_body_dict):
        """Check that request property converted as expected."""
        assert self.convert_request_with_body_to_dict(
            phantom_ammo_with_body_inst.request) == phantom_request_with_body_dict

    def test_bullet_property(self, phantom_ammo_with_body_inst, phantom_bullet_with_body_dict):
        """Check that bullet property converted as expected."""
        assert self.convert_bullet_with_body_to_dict(
            phantom_ammo_with_body_inst.bullet) == phantom_bullet_with_body_dict
