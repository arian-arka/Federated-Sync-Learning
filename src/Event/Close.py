from src.Lib.Stopwatch import ApplicationTime

def onClose(e: Exception | None = None):
    print('on close, e:',e)
    applicationRuntime = ApplicationTime.stop().elapsed()
    print('application runtime', applicationRuntime)
    from src.Provider.db import connection
    for c in connection:
        connection[c].disconnect()
