import requests
from app import celery
from app.libs.url import FactoryURL

from .notify_event import task_notify_event


@celery.task(name="deplete")
def task_deplete(msg, job_id):
    path = FactoryURL.make(path="schedulers")

    post = {
        'body': [{
            '_id': job_id,
            'msg': msg,
            'crawling': True,
            'enabled': False
        }]
    }

    try:
        resource = requests.put(path, json=post)
        return {'status_code': resource.status_code}
    except requests.exceptions.RequestException as error:
        return {'error': str(error)}
