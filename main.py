#!/usr/bin/env python3
import boto3
import queue
import time
import threading

from utils import calc_etag
from worker import Worker
from logger import EventLogger
from jobcrator import JobCreator

POOL_THREADS = 5


def main():
    object_name = 'target.txt'
    # for security reasons I decided to omit my account access key
    access_key = ''
    # for security reasons I decided to omit my account secret key
    secret_key = ''
    etag = calc_etag("target.txt")
    targets = [{'BUCKET_NAME': 'davi17g-us-east-1', 'OBJECT_NAME': object_name,"ETAG": etag},
              {'BUCKET_NAME': 'davi17g-us-east-2', 'OBJECT_NAME': object_name, "ETAG": etag},
              {'BUCKET_NAME': 'davi17g-us-west-1', 'OBJECT_NAME': object_name, "ETAG": etag},
              {'BUCKET_NAME': 'davi17g-us-west-2', 'OBJECT_NAME': object_name, "ETAG": etag}]
    jobsQ = queue.Queue()
    resQ = queue.Queue()

    print("Start S3 Monitor")
    client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    job_creator = JobCreator(targets=targets, interval=59.0, queue=jobsQ)
    logger = EventLogger(file_path="output.log", queue=resQ)
    logger.start()
    job_creator.start()
    workers = []
    for i in range(POOL_THREADS):
        w = Worker(client=client, jobsQ=jobsQ, resQ=resQ)
        w.start()
        workers.append(w)
    time.sleep(3 * 60)

    print("Monitor is terminating")
    for worker in workers:
        worker.close()

    job_creator.close()
    logger.close()

    for th in threading.enumerate():
        if th != threading.main_thread():
            th.join()



if __name__ == '__main__':
    main()