
import requests
from pydash import has, get, from_pairs, map_

from app import celery
from .notify_event import task_notify_event
from .depleted_job import task_deplete
from .chain import task_chain


def call_chains(chain):
    if chain:
        for job in chain:
            task_chain.delay(get(job, '_id'), get(job, 'countdown'))


@celery.task(name="webhook")
def task_webhook(name, id, endpoint, method="GET", params={}, chain=[]):
    normalize = from_pairs(map_(params, lambda i: [i['key'], i['value']]))
    msg = "Scheduler run - %s" % (name)
    result = ''
    notify_id = None
    roles = {
        "_id": id,
        "refs": "scheduler",
        "role": 5
    }

    try:
        resource = requests.request(method, endpoint, data=normalize)
    except requests.exceptions.RequestException as error:
        deple_id = task_deplete.delay(str(error), id)
        return {'msg': result, 'deple_id': deple_id}


    if resource.status_code in [200, 201, 204]:
        result = resource.text
        notify_id = task_notify_event.delay(msg=msg, roles=roles, description=result, status='success')
        call_chains(chain)

    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        result = "ERROR %s" % str(resource.text)
        notify_id = task_notify_event.delay(msg=msg, roles=roles, description=result, status='danger')

    return {'msg': result, 'notify_id': notify_id}