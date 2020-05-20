# Yapam: Yet another ammo generator for Yandex.tank
==============================================


[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
TODO: badge for tests Action
TODO: badge with coverage Action
TODO: badge with build Action
------------------------------------------------------------------------
yapam is a tool that aims to simplify the process of working with Yandex.Tank

### TODO: story why i wrote it

Edit tool config and it automatically creates ammo that you can use for your tests.
For now it can create only Phantom-type ammo.

## Installation
Your Python version should be 3.6 or above. Simply install with python package manager like pip: 
`pip install yapam`

## Configuration
Configuration file should be JSON-type file with .json extension.

### Configuration options:
`LOG_DATE_FMT`: date format for internal logging

`LOG_FMT`: internal logging log format (same as Python basic logging format)

`LOG_LVL`: level of logging (same as Python basic logging levels)

`AMMO_FILE`: path to file where results should be saved

`REQUESTS`: list of requests for your shooting

#### Example:
```
{
  "LOG_DATE_FMT": "%H:%M:%S",
  "LOG_FMT": "%(asctime)s.%(msecs)d|%(levelname).1s|%(message)s",
  "LOG_LVL": "DEBUG",
  "AMMO_FILE": "ammo",
  "REQUESTS": [
    {
      "host": "127.0.0.1",
      "port": 8888,
      "url":  "/auth",
      "method":  "POST",
      "body": "{\"username\": \"admin\", \"password\": \"admin\"}"
    }
  ]
}
```

## Usage
### create local runner, like app.py
```
# -*- coding: utf-8 -*-

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
```

### create template for your future configuration file
`python app.py --template`

### edit configuration file

### run your runner
`python app.py` or `python app.py --config 'my.json'` 

### use your ammo for tank shooting!

## Я все прочитал, но ничего не понял. Что мне делать?
1. Положить api-token от сервиса для онлайн-просмотра результатов в файл token.txt
`echo 'fa30617b49bb4dadb2820fa3511ce420' >> $PYTHONPATH/tests/yandex.tank/token.txt`
2. Актуализировать load.yaml для кейса.
2. Выполнить генерацию патронов для кейса.
3. Запустить контейнер с Yandex.Tank для кейса.
4. Посмотреть результаты на https://overload.yandex.net/ 

###### Запуск контейнера с Yandex.Tank
docker run -v $(pwd):/var/loadtest --net host -it direvius/yandex-tank

## Additional docs
https://yandex.ru/dev/tank/
https://yandextank.readthedocs.io/en/latest/
https://gist.github.com/sameoldmadness/9abeef4c2125bc760ba2f09ee1150330
https://www.youtube.com/watch?v=gws7L3EaeC0
https://overload.yandex.net/
https://yandextank.readthedocs.io/en/latest/ammo_generators.html

## Как мне предложить баг, фичу?
123
