# Federated-Sync-Learning

Directory Structure
- src/App/Controller
  - In here you define your controllers(Different ML models) which extends from the Trainer class
    - ````python
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
      
      ````

- src/Config/*
  - in here you define your config files and are accessible through config('file.key1.key2.key3...') helper by importing it from src.lib.Config import config

- Containerization/Dataset.py
  - in here you need to define two functions
    - splitDatasets(count,round)
    - datasetToJson(dataset)
  - it is used to transfer datasets between models


Inside the Containerization/nodes.json file you need to specify the topology and variables
````json
{
  "rounds": 1,
  "logs_path": "./logs.json",
  "image_name": "image_node_0",
  "container_name_prefix": "container_node_",
  "network": {
    "name": "network_node_0",
    "subnet": "188.18.0.0/16",
    "https": false
  },
  "topology": [
    [
      0,
      1
    ],
    [
      1,
      0
    ]
  ],
  "containers": {
    "0": {
      "container": {
          "cpu": 10,
     "memory": "700mb",
        "port": 50000,
        "ip": "188.18.0.2"
      },
      "env": {
        "host": "0.0.0.0",
        "debug": false,
        "mongodb_uri": "mongodb://172.17.0.1:27018",
        "epochs": 1,
        "threads": 8,
        "port": 50000,
        "break_on_first_communication": false,
        "communication_retries": 2,
         "allowed_aggregation_seconds": 30,
        "allowed_communication_seconds": 30,
        "allowed_calculation_seconds": 500,
        "allowed_test_of_train_seconds": 250,
        "allowed_test_of_aggregation_seconds": 250
      },
      "args": {
      },
      "initialization": []
    },
    "1": {
      "container": {
        "cpu": 10,
        "memory": "700mb",
        "port": 50001,
        "ip": "188.18.0.3"
      },
      "env": {
        "host": "0.0.0.0",
        "debug": false,
        "mongodb_uri": "mongodb://172.17.0.1:27018",
        "epochs": 1,
        "port": 50001,
        "threads": 8,
        "break_on_first_communication": false,
        "communication_retries": 2,
        "allowed_aggregation_seconds": 30,
        "allowed_communication_seconds": 30,
        "allowed_calculation_seconds": 500,
        "allowed_test_of_train_seconds": 250,
        "allowed_test_of_aggregation_seconds": 250
      },
      "args": {
      },
      "initialization": []
    }
  }
}
````

- rounds : specify the aggregation rounds
- logs_path : specify the path of logs to be generated
- image_name : image name for docker to be created
- network :
  - name : specify the name of the network you want to create in the docker
  - subnet : subnet of the network
- topology : it's a 2D matrix that defines how nodes are connected together
- containers : a key-value 
  - key: index of the container that you also use in the topology
  - value : 
    - container : specify cpu,memory,port,ip of the container
    - env : environment variables such as
      - host
      - mongodb_uri
      - epochs : for the learning
      - port 
      - threads : for learning
      - break_on_first_communication : break when the first communication fails
      - communication_retries
      - allowed_aggregation_seconds
      - allowed_communication_seconds
      - allowed_calculation_seconds
      - allowed_test_of_train_seconds
      - allowed_test_of_train_seconds
      - allowed_test_of_aggregation_seconds
    - args : key value passed when running the node as a container such as 
      - python main.py arg1 arg2 ...


### Sample log file for a round and two nodes connected together for GooglenetCifar10
````json
[
  {
    "name": "container_node_0",
    "rounds": [
      {
        "_id": "65dc819546debdd5c6d6cdb9",
        "training_id": "65dc814e46debdd5c6d6cdb8",
        "instance_name": "container_node_0",
        "round": 1,
        "calculation_result": [
          {
            "weight": "c16bf5a9-b57c-466e-b940-acdd9ce7a815.txt"
          },
          {
            "attributes": {},
            "weight": "6f86251d-1863-43b7-be84-08b5b7a8f430.txt"
          }
        ],
        "aggregation_result": {
          "attributes": {},
          "weight": "3b7e9458-55fd-4099-843d-735ea6693b52.txt"
        },
        "test_of_train_result": {
          "score": [
            0.8541861176490784,
            0.7222999930381775
          ]
        },
        "test_of_aggregation_result": {
          "score": [
            0.8541861176490784,
            0.7222999930381775
          ]
        },
        "calculation_time": 234.20166325569153,
        "communication_time": 0.07916831970214844,
        "aggregation_time": 0.0034351348876953125,
        "test_of_train_time": 74.40164828300476,
        "test_of_aggregation_time": 58.66877460479736,
        "calculation_start_datetime": "2024-02-26T12:18:42.214000",
        "calculation_end_datetime": "2024-02-26T12:22:36.416000",
        "communication_start_datetime": "2024-02-26T12:27:06.434000",
        "communication_end_datetime": "2024-02-26T12:27:06.513000",
        "aggregation_start_datetime": "2024-02-26T12:27:13.498000",
        "aggregation_end_datetime": "2024-02-26T12:27:13.502000",
        "test_of_train_start_datetime": "2024-02-26T12:25:24.380000",
        "test_of_train_end_datetime": "2024-02-26T12:26:38.782000",
        "test_of_aggregation_start_datetime": "2024-02-26T12:27:20.546000",
        "test_of_aggregation_end_datetime": "2024-02-26T12:28:19.215000",
        "start_datetime": "2024-02-26T12:18:29.638000",
        "end_datetime": null,
        "error": false,
        "error_messages": []
      }
    ]
  }
]
````