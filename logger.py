import threading


class EventLogger(threading.Thread):

    def __init__(self, file_path, queue):
        threading.Thread.__init__(self)
        self._file_path = file_path
        self._queue = queue
        self._shutdown = False

    def run(self) -> None:
        with open(self._file_path, 'w') as f:
            while not self._shutdown:
                log_row = self._queue.get()
                f.write(log_row + '\n')
                f.flush()

    def close(self):
        self._shutdown = True
