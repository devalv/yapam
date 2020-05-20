# -*- coding: utf-8 -*-
"""Ammo factory test cases."""
import filecmp

import pytest

from yapam.armory import Armory
from yapam.config import ConfigRequest


pytestmark = [pytest.mark.armory]


@pytest.fixture
def config_requests(config_request):
    """List of config requests."""
    request_instance = ConfigRequest(**config_request)
    return [request_instance]


@pytest.fixture
def armory_instance(logger, temporary_ammo_file, config_requests):
    """Fixture with Armory instance."""
    return Armory(requests=config_requests, ammo_file_path=temporary_ammo_file, logger=logger)


@pytest.fixture
def phantom_ammo_blueprint(tmpdir_factory):
    """Fixture that create expected ammo file for compare."""
    fn = tmpdir_factory.mktemp('data').join('ammo')
    data = (
        '192 /auth\n'
        'POST /auth HTTP/1.1\r\n'
        'Host: 127.0.0.1:8888\r\n'
        'User-Agent: phantom\r\n'
        'Accept: */*\r\n'
        'Content-Type: application/json\r\n'
        'Connection: Close\r\n'
        'Content-Length: 42\r\n\r\n'
        '{"username": "admin", "password": "admin"}\r\n\r\n'
    )
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(data)
    return fn


class TestArmory:
    """Armory test cases."""

    def test_init(self, logger, temporary_ammo_file, config_requests):
        """Armory constructor test case."""
        assert isinstance(Armory(requests=config_requests, ammo_file_path=temporary_ammo_file, logger=logger), Armory)

    def test_generate_ammo(self, armory_instance, phantom_ammo_blueprint):
        """Check that armory can generate phantom ammo as expected."""
        assert armory_instance.generate_ammo()
        assert filecmp.cmp(armory_instance.ammo_file_path, phantom_ammo_blueprint)
