# -*- coding: utf-8 -*-
"""Ammo factory test cases."""
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
    """Armory instance."""
    return Armory(requests=config_requests, ammo_file_path=temporary_ammo_file, logger=logger)


@pytest.fixture
def phantom_ammo_blueprint():
    """List of lines that should be in ammo file after script finish."""
    data = [
        '192 /auth',
        'POST /auth HTTP/1.1',
        'Host: 127.0.0.1:8888',
        'User-Agent: phantom',
        'Accept: */*',
        'Content-Type: application/json',
        'Connection: Close',
        'Content-Length: 42',
        '{"username": "admin", "password": "admin"}',
    ]
    return data


class TestArmory:
    """Armory test cases."""

    def test_init(self, logger, temporary_ammo_file, config_requests):
        """Armory constructor test case."""
        assert isinstance(Armory(requests=config_requests, ammo_file_path=temporary_ammo_file, logger=logger), Armory)

    def test_generate_ammo(self, armory_instance, phantom_ammo_blueprint):
        """Check that armory can generate phantom ammo as expected."""
        # Check that ammo generated without errors
        assert armory_instance.generate_ammo()

        # Parse created file to list format
        ammo_lines = list()
        with open(armory_instance.ammo_file_path, 'r') as f:
            for line in f.readlines():
                el = line.strip()
                if el:
                    ammo_lines.append(el)

        # Because of unordered dict in 3.5 lists may be different (headers)
        ammo_lines.sort()
        phantom_ammo_blueprint.sort()

        # Compare list
        assert ammo_lines == phantom_ammo_blueprint
