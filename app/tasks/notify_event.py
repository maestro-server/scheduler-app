import requests
from app import celery
from app.libs.url import FactoryURL


@celery.task(name="scheduler.notify")
def task_notify_event(msg, roles, description='', status='info', context='scheduler'):
    post = {
        'body': [{
            'msg': msg,
            'context': context,
            'description': description,
            'roles': roles,
            'status': status,
            'active': True
        }]
    }

    path = FactoryURL.make(path="events")
    result = requests.put(path, json=post)

    return {'status_code': result.status_code, 'post': post}
