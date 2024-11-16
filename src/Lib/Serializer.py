import json

import numpy as np

from json import dumps,loads,JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def numpyToJson(data):
    return dumps(data,cls=NumpyArrayEncoder)

def writeNumpyToFile(path,data):
    f = open(path,'w')
    f.write(numpyToJson(data))
    f.close()

def readJson(path):
    f = open(path,'r')
    data = json.loads(f.read())
    f.close()
    return data
