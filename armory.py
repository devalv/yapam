# -*- coding: utf-8 -*-

"""Yet another phantom ammo maker."""
import argparse
import sys


# TODO: подключить модное покрытие тестами для github
# TODO: ci/cd
# TODO: readme
# TODO: подключить pytest
#
# pytest.ini
# [pytest]
# addopts = --cov-report=xml --cov=<path> --flake8
# testpaths = <test_paths>
#

from dav_utils.config import Config
from dav_utils.descriptors import (DictType, HttpMethod, IntType,
                                   ListType, StringType, WritableFile)
from dav_utils.utils import Util


class AmmoConfig(Config):
    """Script configuration.

    Factory parameters:
        ammo_file: path to a file where results should be saved
        requests: list of a request-hashes from config
            "REQUESTS": [
                {
                  "host": "127.0.0.1",      # request host parameter (where tank will shoot).
                  "url":  "AUTH",           # server handler URL (where tank will shoot).
                  "method":  "POST",        # request method.
                  "case":  "CONFIG_CASE1",  # test case tag in report.
                  "extra_headers": {}       # additional request headers.
                  "body": "user=user"       # body string (json-type)
                  "port": 443               # port where handler runs. default value is 80. int.
                }
            ]

    script logging:
        log_date_fmt: log date format (only str)
        log_fmt: log format (only str)
        log_lvl: log level (logging.DEBUG, logging.INFO and etc.)
    """

    requests = ListType('requests')
    ammo_file = StringType('ammo_file')

    def create_template(self, file_path: str):
        """Create JSON config file template."""
        config_template = {
            'LOG_DATE_FMT': '%H:%M:%S',
            'LOG_FMT': '%(asctime)s.%(msecs)d|%(levelname).1s|%(message)s',
            'LOG_LVL': 'DEBUG',
            'AMMO_FILE': 'ammo',
            'REQUESTS': [
                {
                    'host': '127.0.0.1',
                    'port': 80,
                    'url': 'AUTH',
                    'method': 'POST',
                    'body': '{\"username\": \"tank_user_0\", \"password\": \"tank_user_0\"}'
                }]
        }
        self.save_json_file(file_path, config_template)
        self.log.info('Template {file_path} created.'.format(file_path=file_path))


class PhantomAmmo:
    """PhantomAmmo blueprint.

    Result should look like:
        234 CONFIG_CASE1
        POST AUTH HTTP/1.1
        Authentication: jwt QWEASDASD
        Host: 127.0.0.1:80
        User-Agent: phantom
        Accept: */*
        Content-Type: application/json
        Connection: Close
        Content-Length: 54

        {"username": "tank_user_0", "password": "tank_user_0"}
    """

    no_body_template = (
        '{method} {url} HTTP/1.1\r\n'
        '{headers}'
    )

    body_template = (
        '{method} {url} HTTP/1.1\r\n'
        '{headers}\r\n'
        'Content-Length: {content_length}\r\n'
        '\r\n'
        '{body}'
    )
    default_headers = {'Host': None,
                       'User-Agent': 'phantom',
                       'Accept': '*/*',
                       'Content-Type': 'application/json',
                       'Connection': 'Close'}

    ammo_template = (
        '{request_length} {case}\n'
        '{request}\r\n\r\n'
    )

    method = HttpMethod('method')
    url = StringType('url')
    host = StringType('host')
    body = StringType('body')
    port = IntType('port')
    extra_headers = DictType('extra_headers')

    def __init__(self, log: Config.log, method: str, url: str, host: str, case: str = None, port: int = 80,
                 extra_headers: dict = None,
                 body: str = None):
        """Phantom-type bullet constructor.

        method: one of allowed http methods.
        url: url where tank will shoot.
        host: host to shoot.
        case: test case tag in report.
        port: port where handler runs.
        extra_headers: request additional headers.
            default_headers are:
                {'Host': None,
                 'User-Agent': 'phantom',
                 'Accept': '*/*',
                 'Content-Type': 'application/json',
                 'Connection': 'Close'}
        body: request body.
        """
        self.log = log
        self.method = method
        self.url = url
        self.host = host

        self.port = port
        self.case = case if case else url

        headers = extra_headers if extra_headers else dict()
        self.default_headers['Host'] = '{host}:{port}'.format(host=self.host, port=self.port)
        headers.update(self.default_headers)

        self.headers = headers
        self.body = body if body else ''

    @property
    def headers(self) -> str:
        """Phantom-type bullet http headers."""
        return self.__headers

    @headers.setter
    def headers(self, value: dict):
        """Phantom-type bullet http headers setter."""
        headers_list = list()
        for key, value in value.items():
            # all key words must be capitalized
            header_key = '-'.join([word.lower().capitalize() for word in key.split('-')])
            header_str = f'{header_key}: {value}'
            headers_list.append(header_str)
        self.__headers = '\r\n'.join(headers_list)

    @property
    def request(self):
        """Phantom-type bullet http request."""
        if self.body:
            return self.body_template.format(method=self.method, url=self.url, headers=self.headers,
                                             content_length=len(self.body), body=self.body)
        return self.no_body_template.format(method=self.method, url=self.url, headers=self.headers)

    @property
    def bullet(self):
        """Phantom-type bullet for tank."""
        request = self.request
        ammo = self.ammo_template.format(request_length=len(request), case=self.case, request=request)
        self.log.debug(ammo.replace('\r\n', ', ').replace('\n', ', '))
        return ammo


class Armory(Util):
    """Tank ammo factory."""

    ammo_file_path = WritableFile('ammo_file_path')

    def __init__(self, requests: str, ammo_file_path: str, logger: Config.log):
        """Armory constructor.

        requests: list of a request-hashes from config
        ammo_file: path to a file where results should be saved
        logger: config logger.
        """
        self.requests = requests
        self.ammo_file_path = ammo_file_path
        self.log = logger

    def generate_ammo(self):
        """Generate and write Phantom ammo to a text file."""
        ammo_gen = (PhantomAmmo(log=self.log, **request).bullet for request in self.requests)
        self.save_text_file(file_path=self.ammo_file_path, txt_data=ammo_gen)


def parse_args():
    """Парсер входных аргументов скрипта."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json', type=str,
                        help='Path to configuration file, ex: config.json')
    parser.add_argument('--template', default=False, type=bool,
                        help='Create config template')
    return parser.parse_args()


def main():  # noqa
    args = parse_args()

    if args.template:
        cfg = AmmoConfig()
        cfg.log.debug('Trying to create template of configuration file.')
        cfg.create_template(args.config)
        cfg.log.debug('Exit.')
        sys.exit(0)

    try:
        user_config = AmmoConfig(args.config)
        user_config.log.debug(f'Configuration file loaded: {user_config.public_attrs()}')

        armory = Armory(user_config.requests, user_config.ammo_file, user_config.log)
        armory.generate_ammo()
    except (AssertionError, FileExistsError) as error_msg:
        user_config.log.critical(str(error_msg))
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
