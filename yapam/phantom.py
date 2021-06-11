# -*- coding: utf-8 -*-
"""Ammo for phantom load generator."""

from json import dumps


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

    def __init__(self, method: str, url: str, host: str, case: str, port: int,
                 extra_headers: dict,
                 body: str,
                 log=None):
        """Phantom-type bullet constructor.

        method: one of allowed http methods.
        url: url where load generator will shoot.
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
        log: logger instance for debug messages.
        """
        self.log = log
        self.method = method
        self.url = url
        self.host = host

        self.port = port
        self.case = case

        headers = extra_headers
        self.default_headers['Host'] = '{host}:{port}'.format(host=self.host, port=self.port)
        headers.update(self.default_headers)

        self.headers = headers
        if body and isinstance(body, dict):
            body = dumps(body)
        self.body = body

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
            header_str = '{key}: {val}'.format(key=header_key, val=value)
            headers_list.append(header_str)
        self.__headers = '\r\n'.join(headers_list)

    @property
    def request(self):
        """Phantom-type bullet http request."""
        if self.body:
            return self.body_template.format(method=self.method, url=self.url,
                                             headers=self.headers,
                                             content_length=len(str(self.body)),
                                             body=self.body)
        return self.no_body_template.format(method=self.method,
                                            url=self.url,
                                            headers=self.headers)

    @property
    def bullet(self):
        """Phantom-type bullet for load generator."""
        request = self.request
        ammo = self.ammo_template.format(request_length=len(request),
                                         case=self.case,
                                         request=request)
        if self.log:
            self.log.debug(ammo.replace('\r\n', ', ').replace('\n', ', '))
        return ammo
