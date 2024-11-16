from fastapi import APIRouter
from src.Provider.db import db
from src.Logic.Trainer import getTrainer
import json
import os
from src.Lib.Config import config
api = APIRouter()

roundCollection = db['learning'].get_collection('rounds')


@api.get('/logs/gather')
async def gatherLogs():

    trainingId = getTrainer()._model['_id']
    rounds = list(roundCollection.find({'training_id': trainingId}).sort('_id', 1))
    if not len(rounds):
        weight = []
    else:
        res = rounds[len(rounds) - 1]['aggregation_result']
        if res and 'weight' in res and res['weight']:
            f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Files', res['weight']) , 'r')
            weight = json.loads(f.read())
            f.close()
        else:
            weight = []

    for r in rounds:
        r['_id'] = str(r['_id'])
        r['training_id'] = str(r['training_id'])

    return {
        'name' : config('server.instance_name'),
        'rounds': rounds,
        # 'final_weight': weight
    }
