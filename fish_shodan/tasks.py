import os
import time

from celery.app import task

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")



@celery.task()
def whois(task_type):
    time.sleep(int(task_type) * 10)
    return True