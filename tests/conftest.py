# -*- coding: utf-8 -*-
"""Common fixtures."""
import logging

import pytest


@pytest.fixture(scope='session')
def temporary_log_file(tmpdir_factory):
    """Temporary log file."""
    return tmpdir_factory.mktemp('data').join('tmp.log')


@pytest.fixture(scope='session')
def temporary_json_file(tmpdir_factory):
    """Temporary JSON file."""
    return tmpdir_factory.mktemp('data').join('cfg.json')


@pytest.fixture
def logger(temporary_log_file):
    """Fixture with logger instance."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(temporary_log_file))
    return logger


@pytest.fixture(scope='session')
def temporary_ammo_file(tmpdir_factory):
    """Temporary ammo file."""
    return str(tmpdir_factory.mktemp('data').join('ammo'))


@pytest.fixture
def config_request():
    """Fixture with parameters in the ConfigRequest."""
    request_dict = {
        'host': '127.0.0.1',
        'port': 8888,
        'url': '/auth',
        'method': 'POST',
        'body': '{\"username\": \"admin\", \"password\": \"admin\"}'
    }
    return request_dict
