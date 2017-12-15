
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
    result = resource.json()

    msg = "Scheduler in %s connection %s on provider %s" % (type, instance_id, provider)
    notify_id = task_notify_event.delay(msg, conn.get('roles'))

    return {'result': result, 'notify_id': notify_id}