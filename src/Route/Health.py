from fastapi import APIRouter,Request
from src.Lib.Config import config

api = APIRouter()

@api.get('/health/check')
async def healthCheck():
    return {'ok': True}

@api.get("/info")
def test(request: Request):
    return {
        "message": "Hello World from {} for {}:{}".format(config('server.instance_name'), request.client.host,
                                                          request.client.port),
        "config": config(),
    }