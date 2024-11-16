import os, sys
from src.Lib.Api import api

def readAll():
    d = os.path.dirname(os.path.abspath(__file__)) + '/../Route'
    sys.path.append(d)
    for (_1, _2, filenames) in os.walk(d):
        for filename in filenames:
            name = filename.split('.')[0]
            exec('import src.Route.{};'.format(name))
            exec('api.include_router(src.Route.{}.api);'.format(name))

readAll()