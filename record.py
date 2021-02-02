import json


class Record(object):

    def __init__(self, time, bucket, status_code=None, latency=None, retry_attempts=None, error=None):
        self._time = time.strftime("%m/%d/%Y, %H:%M:%S")
        self._bucket = bucket
        self._status_code = status_code
        self._retry_attempts = retry_attempts
        self._latency = str(latency)
        self._error = error

    def __repr__(self):
        return json.dumps(self.__dict__)