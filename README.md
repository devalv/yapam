![tests](https://github.com/devalv/yapam/workflows/Linter%20and%20tests/badge.svg)
![build](https://github.com/devalv/yapam/workflows/Build%20Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/devalv/yapam/branch/master/graph/badge.svg)](https://codecov.io/gh/devalv/yapam)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

# Yapam
Yapam is a tool that aims to simplify the process of working with [Yandex Tank](https://github.com/yandex-load/yandex-tank)

Edit tool config and it automatically creates ammo that you can use for your tests.
For now, it can create only Phantom-type ammo. If the app that you need to test is not stateless - probably you should
find another way.

I have nothing to do with the Tank or Yandex itself but was impressed by the great work that they did.
#### Remark
Sooner or later for any project, questions arise:

```
 What load can it handle? 
 Which handlers are slow? 
 What exactly happens if you increase the number of application instances?
```

Your first mind maybe `I should use one of the stress testing tools!`, but if you do not have colleagues who
could do this, then the task will fall on your shoulders. In my opinion, Yandex Tank is an easy and convenient way
to do this type of task (and as far as I know - it is free and opensource).
The right way is to read official docs, but...
Ok, if you want to do it ASAP here is a small Python script that will generate all you need to generate for tank shooting. 

## Installation
Your Python version should be 3.6 or above. Simply install with Python package manager like pip: 
`pip install yapam`

## Configuration
Configuration file should be JSON-type file with .json extension.

### Configuration options:
`LOG_DATE_FMT`: date format for internal logging

`LOG_FMT`: internal logging log format (same as Python basic logging format)

`LOG_LVL`: level of logging (same as Python basic logging levels)

`AMMO_FILE`: a path to file where results should be saved

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
        cfg.log.debug('Trying to create a template of configuration file.')
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

### create a template for your future configuration file
`python app.py --template`

### edit configuration file

### run your runner
`python app.py` or `python app.py --config 'my.json'` 

### use your ammo for tank shooting!

## I read everything, but still did not understand anything. Show me a super short way to run the whole thing?
### 1. Create your ammo via yapam
### 2. Get your personal token on Overload and put it in to a file.
https://overload.yandex.net/
### 3. Edit **load.yaml** for shooting. 
```
phantom:
  address: 127.0.0.1:80
  ssl: false
  load_profile:
    load_type: rps
    schedule: line(1, 10, 1m)
  ammofile: /var/loadtest/ammo  # path inside yandex docker container (step 4)
  ammo_type: phantom
console:
  enabled: true
telegraf:
  enabled: true
uploader:
  enabled: true
  operator: <paste your username>
  package: yandextank.plugins.DataUploader
  token_file: <path to file with tour token> (step 2)
```
### 4. Run docker with Yandex Tank
docker run -v $(pwd):/var/loadtest --net host -it direvius/yandex-tank
### 5. See your results at Overload
https://overload.yandex.net/

## Here are some links to official docs
https://yandex.ru/dev/tank/
https://yandextank.readthedocs.io/en/latest/
https://gist.github.com/sameoldmadness/9abeef4c2125bc760ba2f09ee1150330
https://www.youtube.com/watch?v=gws7L3EaeC0
