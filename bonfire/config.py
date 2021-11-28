import json
from .utils import build_abs_path
from tinydb import TinyDB

# Models options for an application
class ApplicationOptions():
    pass

# Model configuration information from config.json
class Config:
    def __init__(self, db_path, whitelist, max_apps_in_list):
        self.db = TinyDB(build_abs_path(db_path))
        self.whitelist = whitelist
        self.max_apps_in_list = max_apps_in_list

# Open config.json and read contents
PATH_TO_CONFIG = build_abs_path('../store/config.json')
with open(PATH_TO_CONFIG, 'r') as config_file:
    config_opts = json.loads(config_file.read())
configuration = Config(config_opts['db-path'], config_opts['apps']['whitelist'], config_opts['max-apps-shown'])

# Return configuration object
def config():
    return configuration