# -*- coding: utf-8 -*-
"""Ammo factory.

Supported ammo types: Phantom
In most cases, you need this particular module.

Example of usage:
    user_config = AmmoConfig('config.json')
    armory = Armory(user_config.requests, user_config.ammo_file, user_config.log)
    armory.generate_ammo()
"""

from dav_utils.config import Config
from dav_utils.descriptors import WritableFile
from dav_utils.utils import Util

from yapam.phantom import PhantomAmmo


class Armory(Util):
    """Ammo factory.

    requests:       list of ConfigRequest instances, like [ConfigRequest, ]
    ammo_file_path: path to file where result should be saved.
    logger:         your logger instance. Transmitted to ammo class for debug logging. May be None.
    """

    ammo_file_path = WritableFile('ammo_file_path')

    def __init__(self, requests: str, ammo_file_path: str, logger: Config.log):
        """Armory constructor.

        requests:  list of requests from config
        ammo_file: path to a file where results should be saved
        logger:    config logger.
        """
        self.requests = requests
        self.ammo_file_path = ammo_file_path
        self.log = logger

    def generate_ammo(self):
        """Generate and write Phantom ammo to a text file."""
        ammo_gen = (
            PhantomAmmo(log=self.log,
                        method=request.method,
                        url=request.url,
                        host=request.host,
                        case=request.case,
                        port=request.port,
                        extra_headers=request.extra_headers,
                        body=request.body).bullet for request in self.requests
        )
        self.save_text_file(file_path=self.ammo_file_path, txt_data=ammo_gen)
        return True
