from src.Lib.DB.Driver.Connection import Connection
from pymongo import MongoClient

class SyncMongo(Connection):
    def connect(self):
        try:
            self.connection = MongoClient(self.data['uri'])
            print('mongo sync connected')

        except Exception as e:
            print('mongo sync exception',e)
            self.exception = e
        finally:
            return self

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
