import re
import requests
import json

from app import celery

from app.libs.url import FactoryURL
from pydash import from_pairs, map_, pick
from app.tasks.webhook import task_webhook
from app.tasks.depleted_job import task_deplete

def addParams(args, objs):

    for key, val in objs.items():
        args.append({
            'key': key,
            'value': json.dumps(val)
        })

    return objs

@celery.task(name="reports")
def task_reports(name, _id, endpoint, method="GET", source='report', args={}, chain=[]):

    normalize = from_pairs(map_(args, lambda i: [i['key'], i['value']]))

    query = json.dumps({
        '_id': normalize.get('report_id'),
        'owner._id': normalize.get('owner_user'),
        'active': True
    })

    path = FactoryURL.make(path='reports')
    resource = requests.post(path, json={'query': query})
    
    if resource.status_code == 200:
        result = resource.json()
        if result.get('found', 0) == 1:
            objs = pick(result.get('items')[0], ['filters', 'component'])
            addParams(args, objs)

            webhook_id = task_webhook.delay(name, _id, endpoint, source, method, args, chain)
            return {'webhook_id': webhook_id}

        msg = "Report desactived - %s" % _id

    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        msg = resource.text

    deple_id = task_deplete.delay(msg, _id)
    return {'deplete_id': deple_id, 'status_code': resource.status_code}
