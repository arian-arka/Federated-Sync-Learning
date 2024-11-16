import traceback
def onError(e :Exception):
    print('on Error',e)
    traceback.print_tb(e.__traceback__)

