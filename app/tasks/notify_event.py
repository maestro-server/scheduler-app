from app import celery
from app.libs.url import FactoryURL
from app.libs.data_request import data_request

@celery.task(name="scheduler.notify")
def task_notify_event(msg, roles, description='', status='info'):
    post = {
        'body': [{
            'msg': msg,
            'context': 'scheduler',
            'description': description,
            'roles': roles,
            'status': status,
            'active': True
        }]
    }

    path = FactoryURL.make(path="events")
    
    return data_request(path, post)
