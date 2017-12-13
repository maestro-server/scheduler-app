
from app import celery

@celery.task(name="scheduler.request", bind=True)
def task_request(self, result, uri):
    pass