import requests
from app import celery
from app.libs.url import FactoryURL

from .notify_event import task_notify_event


@celery.task(name="crawling")
def task_crawling(ids):
    path = FactoryURL.make(path="schedulers")

    body = []
    for id in ids:
        if id:
            body.append({
                '_id': id,
                '$unset': {'crawling': True, 'run_immediately': True}
            })

    if len(body) > 0:
        post = {
            'body': body
        }

        try:
            resource = requests.put(path, json=post)
            return {'status_code': resource.status_code}
        except requests.exceptions.RequestException as error:
            return {'error': str(error)}
