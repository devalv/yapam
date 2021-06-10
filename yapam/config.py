# -*- coding: utf-8 -*-
"""Project config."""

from dav_utils.config import Config
from dav_utils.descriptors import (DictType, HttpMethod, IntType,
                                   StringType)


class ConfigRequest:
    """Structure of Config.requests list element.

    host:           request host parameter (host where load generator will shoot).
    url:            request url parameter (handler where load generator will shoot).
    method:         request method.
    case:           test case tag in report. default value is url.
    extra_headers:  additional request headers (dict)
    body:           request body string.
    port:           request port where handler runs. default value is 80.
    """

    method = HttpMethod('method')
    url = StringType('url')
    host = StringType('host')
    body = DictType('body')
    port = IntType('port')
    extra_headers = DictType('extra_headers')

    def __init__(self, host: str, url: str, method: str, case: str = None, port: int = 80, extra_headers: dict = None,
                 body: str = None):
        """Validate parameters and create instance of ConfigRequest."""
        self.method = method
        self.url = url
        self.host = host
        self.port = port
        self.case = case if case else url
        self.extra_headers = extra_headers if extra_headers else dict()
        self.body = body if body else dict()


class ConfigRequestType:
    """Descriptor for ConfigRequestType checking."""

    def __init__(self, name):
        """Set attribute name."""
        self.name = name

    def __set__(self, instance, raw_values_list: list):
        """Check that raw_value_list is a list and create ConfigRequest instance for each list element."""
        if isinstance(raw_values_list, list):
            try:
                instance.__dict__[self.name] = [ConfigRequest(**value) for value in raw_values_list]
            except TypeError as E:
                print(E)
                raise TypeError('{} contains bad parameters.'.format(self.name))
        else:
            raise TypeError('{} should be a list.'.format(self.name))

    def __get__(self, instance, class_):
        """Return attribute value."""
        return instance.__dict__[self.name]


class AmmoConfig(Config):
    """Script configuration.

    Factory parameters:
        ammo_file: path to a file where results should be saved
        requests: list of a request-hashes from config
            "REQUESTS": [
                {
                  "host": "127.0.0.1",      # request host parameter (where load generator will shoot).
                  "url":  "AUTH",           # server handler URL (where load generator will shoot).
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

    requests = ConfigRequestType('requests')
    ammo_file = StringType('ammo_file')

    @property
    def template_blueprint(self):
        """Template blueprint."""
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
                    'body': {'username': 'tank_user_0', 'password': 'tank_user_0'}
                }]
        }
        return config_template

    def create_template(self, file_path: str):
        """Create JSON config file template."""
        self.save_json_file(file_path, self.template_blueprint)
        self.log.info('Template {file_path} created.'.format(file_path=file_path))
