
from app import celery

@celery.task(name="tasks.add")
def add(a, b):
    print(a+b)
    return a+b
