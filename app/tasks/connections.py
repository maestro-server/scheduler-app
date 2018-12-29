import re
import requests
import json

from app import celery

from app.tasks.webhook import task_webhook
from app.tasks.depleted_job import task_deplete
from app.repository.externalMaestroScheduler import ExternalMaestroScheduler


@celery.task(name="connections")
def task_connections(name, _id, endpoint, source='discovery', method="GET", args={}, chain=[]):
    msg = "Task Connection - %s" % _id

    try:
        connType = re.search(r'/[a-zA-Z0-9]{24,24}/([a-z-]*)$', endpoint).group(1)
        conn_id = re.search(r'/([a-zA-Z0-9]{24,24})/', endpoint).group(1)

    except Exception as error:
        deple_id = task_deplete.delay(str(error), _id)
        return {'msg': 'Missing type or id', 'deple_id': deple_id}

    process = 'process.%s.state' % connType
    query = json.dumps({
        '_id': conn_id,
        'status': 'enabled',
        'active': True,
        process: {'$ne': 'danger'}
    })

    resource = ExternalMaestroScheduler(_id) \
        .post_request(path="connections", body={'query': query})

    if resource.get_status() >= 400:
        msg = resource.get_error()
        task_deplete.delay(msg, _id)

    if resource.get_status() < 400:
        result = resource.get_results()
        msg = "Connection success - %s" % conn_id
        if result.get('found', 0) == 1:
            webhook_id = task_webhook.delay(name, _id, endpoint, source, method, args, chain)
            return {'webhook_id': webhook_id}

    return {'msg': msg, 'status_code': resource.get_status()}