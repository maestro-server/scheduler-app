
from app import celery
import requests
from app.libs.url import FactoryURL

from .notify_event import task_notify_event

@celery.task(name="scheduler.request", bind=True)
def task_request(self, conn, type):

    provider = conn.get('provider')
    instance_id = conn.get('_id')

    path = FactoryURL.make(path="crawler/%s/%s/%s" % (provider, instance_id, type))
    resource = requests.put(path)

    if resource.status_code == 200:
        result = resource.json()
        msg = "Scheduler in %s connection %s on provider %s" % (type, instance_id, provider)
        notify_id = task_notify_event.delay(msg, conn.get('roles'), 'sucess')

        return {'result': result, 'notify_id': notify_id}

    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        msg = "ERROR %s" % (resource.text)
        notify_id = task_notify_event.delay(msg, conn.get('roles'), 'danger')

        return {'error': msg, 'notify_id': notify_id}