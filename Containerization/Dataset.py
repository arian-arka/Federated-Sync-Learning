from keras.datasets import mnist
import json
from json import JSONEncoder
import numpy as np
import random

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def getDatasets():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # np.random.shuffle(X_train)
    # np.random.shuffle(y_train)

    return {
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test,
    }


def splitDatasets(count, round):
    dataset = getDatasets()

    trainDiff = len(dataset['X_train']) // count  # offsets
    testDiff = len(dataset['X_test']) // count  # offsets

    # lenAll = dataset['X_train'].shape[0]
    # indixes = [x for x in range(lenAll)]
    # random.shuffle(indixes)
    # counter = 0
    # for index in indixes:
    #     dataset['X_train'][counter],dataset['X_train'][index] = dataset['X_train'][index],dataset['X_train'][counter]
    #     dataset['y_train'][counter],dataset['y_train'][index] = dataset['y_train'][index],dataset['y_train'][counter]
    #     counter += 1



    data = [
        {
            'train': {
                'x': dataset['X_train'][i * count:i * count + trainDiff],
                'y': dataset['y_train'][i * count:i * count + trainDiff],
            },
            'test': {
                # 'x': dataset['X_test'][i * count:i * count + testDiff],
                # 'y': dataset['y_test'][i * count:i * count + testDiff],
                'x': dataset['X_test'],
                'y': dataset['y_test'],
            },
        } for i in range(count)
    ]

    return data

def datasetToJson(dataset):
    return json.dumps(dataset, cls=NumpyArrayEncoder)
