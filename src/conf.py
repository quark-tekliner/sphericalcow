import json
import os


class Conf(object):

    _settings = None

    @classmethod
    def get(cls, name, default=None):
        if cls._settings is None:
            settings_file = os.environ.get('SETTINGS') or './settings.json'
            cls._settings = json.load(open(settings_file))
        return cls._settings.get(name, default)
