import json
import time
import numpy
import src.Lib.Serializer
from Lib.Stopwatch import Stopwatch, runWithTimeout
import requests
import datetime
from Lib.Variable import gather, merge
from src.Provider.db import db
from src.Provider.trainer import trainer as trainerController

import uuid
import os
import traceback

roundCollection = db['learning'].get_collection('rounds')

trainingCollection = db['learning'].get_collection('trainings')

_self_lock_counter = 0


def isReady():
    return not _self_lock_counter


def doAndUnluck(callback, **args):
    global _self_lock_counter
    _self_lock_counter += 1
    callback(**args)
    _self_lock_counter -= 1


class Round:
    def setPreCalcResult(self):
        if self._props['round'] == 1:
            self.updateModel({
                '$push': {
                    'calculation_result': {
                        'weight': self.saveNewfile(self._trainerControllerObj.getInitWeight())
                    }
                }
            })
        else:
            res = roundCollection.find_one({
                'training_id': self._props['training_id'],
                'round': self._props['round'] - 1
            },)['aggregation_result']
            self.updateModel({
                '$push': {
                    'calculation_result': res
                }
            })

    def generateModel(self):

        data = {
            'training_id': self._props['training_id'],
            'instance_name': self._props['instance_name'],
            'round': self._props['round'],

            'calculation_result': [],  # [{path_of_weight,accuracy}]

            'aggregation_result': None,  # [{path_of_weight,accuracy}]

            # 'neighbors_weights': [], # [{path_of_weight,instance}]

            'test_of_train_result': None,  # [{path_of_weight,accuracy}]
            'test_of_aggregation_result': None,  # [{path_of_weight,accuracy}]

            'calculation_time': None,
            'communication_time': None,
            'aggregation_time': None,
            'test_of_train_time': None,
            'test_of_aggregation_time': None,

            'calculation_start_datetime': None,
            'calculation_end_datetime': None,

            'communication_start_datetime': None,
            'communication_end_datetime': None,

            'aggregation_start_datetime': None,
            'aggregation_end_datetime': None,

            'test_of_train_start_datetime': None,
            'test_of_train_end_datetime': None,

            'test_of_aggregation_start_datetime': None,
            'test_of_aggregation_end_datetime': None,

            'start_datetime': datetime.datetime.now(),
            'end_datetime': None,

            'error': False,
            'error_messages': [],
        }

        _id = roundCollection.insert_one(data).inserted_id

        self._model = roundCollection.find_one({'_id': _id})

        return self._model

    def updateModel(self, data):
        roundCollection.update_one({'_id': self._model['_id']}, data)

        self._model = roundCollection.find_one({'_id': self._model['_id']})

        return self._model

    def refreshModel(self):
        self._model = roundCollection.find_one({'_id': self._model['_id']})
        return self._model

    def receiveModel(self, instance, weight):
        self._neighbors_weights[instance] = weight
        # self.saveNewfile(weight,'{}.json'.format(instance))

    def setDataset(self, dataset):
        self._dataset = dataset

    def __init__(self, props):
        self._props = props
        self.generateModel()
        self._trainerController = trainerController
        self._neighbors_weights = {}

    def setTrainer(self, trainer):
        self._trainerController = trainer
        return self

    def saveNewfile(self, data, name=None):
        file = '{}.txt'.format(str(uuid.uuid4())) if name is None else name
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Files', file)

        src.Lib.Serializer.writeNumpyToFile(path, data)

        return file

    def runPreCalculation(self):
        self._trainerControllerObj = self._trainerController({})

        self._trainerControllerObj.init(self._dataset)

        self.setPreCalcResult()

    def runCalculation(self):

        def epochUpdator(weight, attributes):
            self.updateModel({
                '$push': {
                    'calculation_result': {
                        'attributes': attributes,
                        'weight': self.saveNewfile(weight)
                    }
                }
            })

        def roundCalculator():
            for i in range(self._props['epochs']):
                self._trainerControllerObj.epoch(epochUpdator)

        def runCalc():
            return runWithTimeout(
                self._props['allowed_calculation_seconds'],
                roundCalculator,
            )

        startDateTime = datetime.datetime.now()

        result = Stopwatch.timeFunction(runCalc)

        data = {
            '$set': {
                'calculation_start_datetime': startDateTime,
                'calculation_end_datetime': datetime.datetime.now(),
                'calculation_time': result['time'],
            }
        }

        if result['error']:
            data['$set']['error'] = True
            data['$push'] = {'error_messages': str(result['result'])}

        self.updateModel(data)

        return not result['error']

    def comminucateWithNeighbor(self, neighbor):
        strData = src.Lib.Serializer.numpyToJson({
            'weight': self._trainerControllerObj.currentWeight(),
            'instance': self._props['instance_name']
        })

        res = requests.post(neighbor + '/trainer/round/receive-model', data=strData, headers={
            'Content-Type': 'application/json'
        })
        if not res.ok:
            raise Exception('Response status is {}'.format(res.status_code))

    def comminucateWithNeighbors(self):
        hasError = False

        for neighbor in self._props['neighbors']:
            communicationResult = True
            for i in range(self._props['communication_retries']):
                try:
                    self.comminucateWithNeighbor(neighbor)
                    break
                except Exception as e:
                    traceback.print_exception(e)
                    communicationResult = e
            if communicationResult is not True:
                self.updateModel({
                    '$push': {'error_messages': str(communicationResult)},
                    '$set': {'error': True},
                })
                hasError = True
                if self._props['break_on_first_communication']:
                    break

        return not hasError

    def runCommunication(self):
        def runCommunicator():
            return runWithTimeout(self._props['allowed_communication_seconds'],
                                  self.comminucateWithNeighbors)

        startDateTime = datetime.datetime.now()

        result = Stopwatch.timeFunction(runCommunicator)

        self.updateModel({
            '$set': {
                'communication_start_datetime': startDateTime,
                'communication_end_datetime': datetime.datetime.now(),
                'communication_time': result['time'],
            }
        })

        return not result['error']

    def runAggregation(self):
        def aggregationUpdator(weight, attributes):
            self.updateModel({
                '$set': {
                    'aggregation_result': {
                        'attributes': attributes,
                        'weight': self.saveNewfile(weight)
                    }
                }
            })

        def runAggregator():
            return runWithTimeout(
                self._props['allowed_aggregation_seconds'],
                self._trainerControllerObj.aggregate,
                weights=self._neighbors_weights.values(),
                save=aggregationUpdator,
            )

        startDateTime = datetime.datetime.now()

        result = Stopwatch.timeFunction(runAggregator)

        data = {
            '$set': {
                'aggregation_start_datetime': startDateTime,
                'aggregation_end_datetime': datetime.datetime.now(),
                'aggregation_time': result['time'],
                'aggregation_result':
                    self._model['calculation_result'][len(self._model['calculation_result']) - 1]
                    if result['error'] else
                    self._model['aggregation_result']
            }
        }

        if result['error']:
            data['$set']['error'] = True
            data['$push'] = {'error_messages': str(result['result'])}

        self.updateModel(data)

        return not result['error']

    def runTestOfTrain(self):
        def testUpdator(attributes):
            self.updateModel({
                '$set': {
                    'test_of_train_result': attributes,
                }
            })

        def runTest():
            return runWithTimeout(
                self._props['allowed_test_of_train_seconds'],
                self._trainerControllerObj.testOfTrain,
                save=testUpdator,
            )

        startDateTime = datetime.datetime.now()

        result = Stopwatch.timeFunction(runTest)

        data = {
            '$set': {
                'test_of_train_start_datetime': startDateTime,
                'test_of_train_end_datetime': datetime.datetime.now(),
                'test_of_train_time': result['time'],
            }
        }

        if result['error']:
            data['$set']['error'] = True
            data['$push'] = {'error_messages': str(result['result'])}

        self.updateModel(data)

        return not result['error']

    def runTestOfAggregation(self):
        def testUpdator(attributes):
            self.updateModel({
                '$set': {
                    'test_of_aggregation_result': attributes,
                }
            })

        def runTest():
            return runWithTimeout(
                self._props['allowed_test_of_aggregation_seconds'],
                self._trainerControllerObj.testOfTrain,
                save=testUpdator,
            )

        startDateTime = datetime.datetime.now()

        result = Stopwatch.timeFunction(runTest)

        data = {
            '$set': {
                'test_of_aggregation_start_datetime': startDateTime,
                'test_of_aggregation_end_datetime': datetime.datetime.now(),
                'test_of_aggregation_time': result['time'],
            }
        }

        if result['error']:
            data['$set']['error'] = True
            data['$push'] = {'error_messages': str(result['result'])}

        self.updateModel(data)

        return not result['error']


class Trainer:
    def __init__(self, props):
        self._props = props
        self._generateModel()
        self._round = 1

    def receiveModel(self, instance, weight):
        self._roundObj.receiveModel(instance, weight)

    def _generateModel(self):
        _id = trainingCollection.insert_one({
            'lock': True,
            'instance_name': self._props['instance_name'],
            'start_datetime': datetime.datetime.now()
        }).inserted_id
        self._model = trainingCollection.find_one({'_id': _id})
        return self._model

    def unlockModel(self, lock):
        self._updateModel({'$set': {'lock': lock}})
        return self

    def _refreshModel(self):
        self._model = trainingCollection.find_one({'_id': self._model['_id']})
        return self._model

    def _updateModel(self, data):
        trainingCollection.update_one({'_id': self._model['_id']}, data)
        self._model = trainingCollection.find_one({'_id': self._model['_id']})
        return self._model

    def _canStart(self):
        while self._refreshModel()['lock']: time.sleep(0.5)

    def receiveDataset(self, dataset):
        self._dataset = dataset

        roundProps = merge(gather(self._props, [
            'instance_name',
            'allowed_calculation_seconds',
            'allowed_communication_seconds',
            'allowed_aggregation_seconds',
            'allowed_test_of_train_seconds',
            'allowed_test_of_aggregation_seconds',
            'communication_retries',
            'break_on_first_communication',
            'epochs',
            'neighbors',
        ]), {
                               'training_id': self._model['_id'],
                               'round': self._round,
                           })
        self._roundObj = Round(roundProps)

        self._roundObj.setDataset(self.getDatasetOfRound(self._round))

    def getDatasetOfRound(self, round):
        # todo
        return self._dataset

    def model(self):
        return self._model

    def preCalculation(self, round):
        time.sleep(0.2)

        self._roundObj.runPreCalculation()

    def calculate(self, round):
        self._canStart()

        result = self._roundObj.runCalculation()

    def communicate(self, round):
        self._canStart()

        result = self._roundObj.runCommunication()

    def aggregate(self, round):
        self._canStart()

        result = self._roundObj.runAggregation()

    def testOfTrain(self, round):
        self._canStart()

        result = self._roundObj.runTestOfTrain()


    def testOfAggregation(self, round):
        self._canStart()

        result = self._roundObj.runTestOfAggregation()

        self._round += 1

    def finish(self):
        self._updateModel({
            '$set': {'end_datetime': datetime.datetime.now()},
        })

_trainer = None


def getTrainer():
    global _trainer
    return _trainer


def makeTrainer(props):
    global _trainer
    _trainer = Trainer(props)
    return _trainer
