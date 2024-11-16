import abc

class Trainer:
    def __init__(self,props):
        self._props = props

    def previousWeight(self):
        return self._previous_weight

    def setPreviousWeight(self,w):
        self._previous_weight = w
        return self

    @abc.abstractmethod
    def getInitWeight(self):
        pass

    @abc.abstractmethod
    def currentWeight(self):
        pass

    @abc.abstractmethod
    def init(self,dataset):
        pass

    @abc.abstractmethod
    def epoch(self,save):
        pass

    @abc.abstractmethod
    def testOfTrain(self,save):
        pass

    @abc.abstractmethod
    def aggregate(self,weights,save):
        pass

    @abc.abstractmethod
    def testOfAggregation(self,save):
        pass




