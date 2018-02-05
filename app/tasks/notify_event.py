
import requests, datetime
from app import celery
from app.libs.url import FactoryURL

@celery.task(name="scheduler.notify", bind=True)
def task_notify_event(self, msg, roles, context = 'scheduler'):

    post = {
        'body': [{
            'msg': msg,
            'context': context,
            'roles': roles,
            'active': True
        }]
    }

    path = FactoryURL.make(path="events")
    result = requests.put(path, json=post)

    return {'status_code': result.status_code, 'post': post}