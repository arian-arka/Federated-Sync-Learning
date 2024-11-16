from fastapi import APIRouter, Request, Body, BackgroundTasks

api = APIRouter()
from src.Logic.Trainer import getTrainer, makeTrainer, isReady, doAndUnluck
from src.Lib.Config import config
from src.Lib.Variable import merge, gather


@api.post('/trainer/init')
async def trainerInit(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda:
                    makeTrainer(merge(
                        {
                            'initialized_weight': body
                        },
                        gather(config('server'), [
                            'instance_name',
                            'allowed_calculation_seconds',
                            'allowed_communication_seconds',
                            'allowed_aggregation_seconds',
                            'allowed_test_of_train_seconds',
                            'allowed_test_of_aggregation_seconds',
                            'communication_retries',
                            'break_on_first_communication',
                            'epochs',
                            'rounds',
                            'neighbors',
                        ])
                    )))

    background_tasks.add_task(func)

    return {

    }


@api.get('/trainer/ready')
async def trainerReady(background_tasks: BackgroundTasks):
    return {
        'ok': getTrainer() is not None and isReady() and not len(background_tasks.tasks)
    }


@api.post('/trainer/dataset')
async def trainerDataset(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().receiveDataset(body))

    background_tasks.add_task(func)

    return {

    }


@api.post('/trainer/lock')
async def trainerLock(body=Body(...)):
    getTrainer().unlockModel(body['lock'])
    return {}


@api.post('/trainer/round/init')
async def trainerRoundInit(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().preCalculation(body['round']))

    background_tasks.add_task(func)

    return {

    }


@api.post('/trainer/round/calculate')
async def trainerRoundCalculate(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().calculate(body['round']))

    background_tasks.add_task(func)

    return {

    }


@api.post('/trainer/round/communicate')
async def trainerRoundCommunicate(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().communicate(body['round']))

    background_tasks.add_task(func)

    return {

    }


@api.post('/trainer/round/receive-model')
async def receiveWeight(body=Body(...)):
    getTrainer().receiveModel(
        body['instance'],
        body['weight']
    )
    return {}


@api.post('/trainer/round/aggregate')
async def trainerRoundAggregate(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().aggregate(body['round']))

    background_tasks.add_task(func)

    return {

    }

@api.post('/trainer/round/test/train')
async def trainerRoundTest(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().testOfTrain(body['round']))

    background_tasks.add_task(func)

    return {

    }

@api.post('/trainer/round/test/aggregation')
async def trainerRoundAggregation(background_tasks: BackgroundTasks, body=Body(...)):
    def func():
        doAndUnluck(lambda: getTrainer().testOfAggregation(body['round']))

    background_tasks.add_task(func)

    return {

    }

@api.get('/trainer/finish')
async def finish(background_tasks: BackgroundTasks):
    def t():
        getTrainer().finish()

    background_tasks.add_task(t)
    return {}
