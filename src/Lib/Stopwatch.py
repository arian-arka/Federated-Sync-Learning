from time import time
import signal
import asyncio
import traceback


class Stopwatch:
    def clear(self):
        self._start = None
        self._stop = None
        self._laps = []
        return self

    def __init__(self):
        self.clear()

    def start(self):
        self.clear()
        self._start = time()
        return self

    def lap(self):
        if self._start is None:
            raise Exception('Stopwatch is not started')
        now = time()
        if not len(self._laps):
            self._laps.append((now, now - self._start, now - self._start))
        else:
            self._laps.append((now, now - self._start(), now - self._laps[len(self._laps) - 1][0]))
        return self

    def lastLap(self):
        return None if not len(self._laps) else self._laps[0]

    def laps(self):
        return self._laps

    def stop(self):
        if self._start is None:
            raise Exception('Stopwatch is not started')
        self._stop = time()
        return self

    def elapsed(self):
        if self._stop is None:
            return time() - self._start
        return self._stop - self._start

    @staticmethod
    def timeFunction(callback, **args):
        s = Stopwatch().start()
        error = False

        try:
            result = callback(**args)
        except Exception as e:
            traceback.print_exception(e)
            error = True
            result = e

        return {
            'time': s.stop().elapsed(),
            'result': result,
            'error': error,
        }

def runWithTimeout(_seconds,callback,**kwargs):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            raise e

    future = asyncio.wait_for(loop.run_in_executor(None,lambda : callback(**kwargs)), _seconds)

    try:
        return loop.run_until_complete(future)
    except Exception as e:
        traceback.print_exception(e)
        raise Exception('Timeout exception')


ApplicationTime = Stopwatch().start()
