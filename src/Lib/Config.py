import os, sys


class _Config:
    def __init__(self):
        all = {}

        d = os.path.dirname(os.path.abspath(__file__)) + '/./../Config'
        sys.path.append(d)

        for (_1, _2, filenames) in os.walk(d):
            for filename in filenames:
                name = filename.split('.')[0]
                exec('import src.Config.{}; all["{}"] = src.Config.{}.conf'.format(name, name, name))

        self.all = all

    def get(self, conf: str = None, default=None):
        if conf is None:
            return self.all

        v = self.all
        for key in conf.split('.'):
            if key in v:
                v = v[key]
            else:
                return default
        return default if v == '' or v is None else v


Config = _Config()


def config(key: str = None, default=None):
    return Config.get(key, default)
