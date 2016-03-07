# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import importlib
import os

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'

COMPILED_CONFIG = importlib.import_module(os.environ.get('APPLICATION_NAME', 'app') + '.cache.config')
COMPILED_CONFIG = getattr(COMPILED_CONFIG, 'COMPILED_CONFIG')


def get_config(name, default=None):
    name = name.split('.')
    config = COMPILED_CONFIG

    for config_part in name:
        if not config.get(config_part):
            return default
        config = config.get(config_part)
    return config