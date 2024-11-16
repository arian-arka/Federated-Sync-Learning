import abc


class Connection:
    def __init__(self,data={}):
        self.data = data
        self.connection = None
        self.exception = None
        self.events = {
            'connect' : [],
            'disconnect' : []
        }

    def event(self,event):
        for e in self.events[event]:
            e()

    @abc.abstractmethod
    def disconnect(self):
        """Implement your code here with data provided and self.event('disconnect') and return your connection"""
        return self

    @abc.abstractmethod
    def connect(self):
        """Implement your code here with data provided and then call self.event('connect') and  return your connection"""
        return self

    def onConnect(self,callback):
        self.events['connect'].append(callback)
        return self

    def onDisconnect(self,callback):
        self.events['disconnect'].append(callback)
        return self

    def isConnected(self):
        return self.connection is not None