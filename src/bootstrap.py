import os, sys
from src.Lib.Config import config

def bootstrap():

    d = os.path.dirname(os.path.abspath(__file__)) + '/../Provider'
    sys.path.append(d)
    for (_1, _2, filenames) in os.walk(d):
        for filename in filenames:
            name = filename.split('.')[0]
            exec('import src.Provider.{};'.format(name))
