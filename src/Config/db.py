from src.Lib.Env import env

conf = {
    'mongo': {
        'uri': env('mongodb_uri','mongodb://127.0.0.1:27017')
    },
}
