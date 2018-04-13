
from app import celery

@celery.task(name="tasks.add", bind=True)
def add(self, a, b):
    print(a, b)
