import os
from configparser import ConfigParser

import click


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    def __init__(self):
        pass

    def lookup_configfile(self):
        pass

