import threading
from record import Record
from datetime import datetime


class Worker(threading.Thread):

    def __init__(self, client, jobsQ, resQ):
        threading.Thread.__init__(self)
        self._client = client
        self._jobsQ = jobsQ
        self._resQ = resQ
        self._shutdown = False

    def run(self) -> None:
        while not self._shutdown:
            job = self._jobsQ.get()
            bucket_name = job['BUCKET_NAME']
            object_name = job['OBJECT_NAME']
            etag = job['ETAG']

            try:
                then = datetime.now()
                obj = self._client.get_object(Bucket=bucket_name, Key=object_name)
                metadata = obj['ResponseMetadata']
                staus_code = metadata['HTTPStatusCode']
                retry_attempts = metadata['RetryAttempts']
                error = ""
                if obj['ETag'] != etag:
                    error = "Corrupted tag"
                now = datetime.now()
                latency = now - then
                self._resQ.put(repr(Record(
                    time=now,
                    bucket=bucket_name,
                    status_code=staus_code,
                    latency=latency,
                    retry_attempts=retry_attempts,
                    error=error
                )))
            except (self._client.exceptions.NoSuchKey, self._client.exceptions.InvalidObjectState) as e:
                self._resQ.put(repr(Record(time=datetime.now(), bucket=bucket_name, error=e)))

    def close(self):
        self._shutdown = True
