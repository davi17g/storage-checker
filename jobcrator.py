import threading
import itertools

from datetime import datetime


class JobCreator(threading.Thread):

    def __init__(self, targets, interval, queue):
        threading.Thread.__init__(self)
        self._shutdown = False
        self._targets = targets
        self._interval = interval
        self._queue = queue

    def run(self) -> None:
        for target in itertools.cycle(self._targets):
            if self._shutdown:
                return
            now = datetime.timestamp(datetime.now())
            try:
                then = target['ts']
                if now - then >= self._interval:
                    target['ts'] = now
                    self._queue.put(target)
            except KeyError:
                target['ts'] = now
                self._queue.put(target)

    def close(self):
        self._shutdown = True
