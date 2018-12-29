from app import celery
from app.repository.externalMaestroData import ExternalMaestroData

@celery.task(name="scheduler.notify")
def task_notify_event(msg, roles, description='', status='info'):

    body = {
        'body': [{
            'msg': msg,
            'context': 'scheduler',
            'description': description,
            'roles': roles,
            'status': status,
            'active': True
        }]
    }

    return ExternalMaestroData() \
        .put_request(path="events", body=body) \
        .get_results()
