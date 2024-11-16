import numpy
import os
import numpy as np

import src.Lib.Serializer
from src.Lib.Config import config

np.random.seed(10)
# from keras.datasets import mnist
from keras.models import Sequential
import tensorflow
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.layers.core import Dense, Dropout, Activation, Flatten

from src.Lib.Controller import Trainer
from src.App.Controller.Model import model as modelObj

class TestTrainer(Trainer):
    def makeModel(self,shape):
        if modelObj.hasKey('model'):
            return
        model = Sequential()
        model.add(Dense(512, input_shape=(784,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))
        model.add(Dense(10))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.build(shape)
        modelObj.set('model',model)

    def getInitWeight(self):
        return modelObj.get('model').get_weights()

    def currentWeight(self):
        return modelObj.get('model').get_weights()

    def init(self, dataset):

        # (X_train, y_train), (X_test, y_test) = mnist.load_data()
        # print(dataset)
        # train = dataset['train']
        # test = dataset['test']
        # (X_train, y_train,) = train
        # (X_test, y_test) = test

        X_train = numpy.asarray(dataset['train']['x'])
        y_train = numpy.asarray(dataset['train']['y'])
        X_test = numpy.asarray(dataset['test']['x'])
        y_test = numpy.asarray(dataset['test']['y'])


        print('Shape of X_train',numpy.shape(X_train))
        print('Shape of y_train',numpy.shape(y_train))
        print('Shape of X_test',numpy.shape(X_test))
        print('Shape of y_test',numpy.shape(y_test))

        X_train = X_train.reshape(numpy.shape(X_train)[0], 784)
        X_test = X_test.reshape(numpy.shape(X_test)[0], 784)
        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')
        X_train /= 255
        X_test /= 255
        no_classes = 10
        Y_train = np_utils.to_categorical(y_train, no_classes)
        Y_test = np_utils.to_categorical(y_test, no_classes)

        self.makeModel(X_train.shape)

        self._X_train = X_train
        self._X_test = X_test
        self._Y_train = Y_train
        self._Y_test = Y_test

    def epoch(self, save):
        model = modelObj.get('model')

        history = model.fit(self._X_train, self._Y_train,
                                  batch_size=128, epochs=1,
                                  verbose=1)
        # score = model.evaluate(self._X_test, self._Y_test)

        weight = model.get_weights()

        save(weight, {
            # 'score': score
            # 'accuracy' : 97.4
        })  # weights,attributes

    def testOfTrain(self,save):
        model = modelObj.get('model')
        score = model.evaluate(self._X_test, self._Y_test)
        save({'score':score})

    def aggregate(self, weights, save):
        model = modelObj.get('model')

        averaged = model.get_weights()

        weights = [
            [numpy.asarray(_w) for _w in w]
            for w in weights
        ]
        for i in range(len(averaged)):
            for j in weights:
                averaged[i] += j[i]
            averaged[i] /= len(weights) + 1

        model.set_weights(averaged)

        save(averaged, {})

    def testOfAggregation(self,save):
        model = modelObj.get('model')
        score = model.evaluate(self._X_test, self._Y_test)
        save({'score':score})