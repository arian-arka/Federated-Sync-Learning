import os
from src.Lib.Variable import Convert

ENV={}
for name, value in os.environ.items():
    ENV[name] = Convert.tryAll(value)

def env(key = None, default=None):
    if key is None:
        return ENV
    v = ENV[key] if key in ENV else None
    return default if v == '' or v is None else v
