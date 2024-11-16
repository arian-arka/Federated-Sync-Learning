from src.Lib.DB.Driver.SyncMongo import SyncMongo
from src.Lib.Config import config

connection = {
    # 'mongo': Mongo(config('db.mongo')).connect(),
    'mongo': SyncMongo(config('db.mongo')).connect(),
}

db = {
    'learning' : connection['mongo'].connection.get_database('learning')
}

