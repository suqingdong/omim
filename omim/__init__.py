import os
import json


HOME = os.path.expanduser('~')
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))

__version__ = version_info['version']

DEFAULT_DB = os.path.join(BASE_DIR, 'data', 'omim.sqlite3')

if not os.path.isfile(DEFAULT_DB):
    DEFAULT_DB = os.path.join(HOME, 'omim_data', 'omim.sqlite3')

DEFAULT_URL = 'https://mirror.omim.org'
