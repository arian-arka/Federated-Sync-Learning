from src.Lib.DB.Driver.Connection import Connection
import motor.motor_asyncio

class Mongo(Connection):
    def connect(self):
        try:
            self.connection = motor.motor_asyncio.AsyncIOMotorClient(self.data['uri'])
            print('mongo connected')

        except Exception as e:
            print('mongo exception',e)
            self.exception = e
        finally:
            return self

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
