# -*- coding: utf-8 -*-
"""Just example of runner."""

import argparse
import sys
from distutils.util import strtobool

from yapam.armory import Armory
from yapam.config import AmmoConfig


def parse_args():
    """Script arguments parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.json', type=str,
                        help='Path to configuration file, ex: config.json')
    parser.add_argument('--template', default=False, type=strtobool, nargs='?', const=True,
                        help='Create config template')
    return parser.parse_args()


def main():
    """Will work when script running directly."""
    args = parse_args()

    if args.template:
        cfg = AmmoConfig()
        cfg.log.debug('Trying to create template of configuration file.')
        cfg.create_template(args.config)
        cfg.log.debug('Exit.')
        sys.exit(0)

    try:
        user_config = AmmoConfig(args.config)
        user_config.log.debug('Configuration file loaded: {}'.format(user_config.public_attrs()))

        armory = Armory(user_config.requests, user_config.ammo_file, user_config.log)
        armory.generate_ammo()
    except (AssertionError, FileExistsError) as error_msg:
        user_config.log.critical(str(error_msg))
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
