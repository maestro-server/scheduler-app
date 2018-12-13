import re
import requests
import json

from app import celery

from app.libs.url import FactoryURL
from app.tasks.webhook import task_webhook
from app.tasks.depleted_job import task_deplete


@celery.task(name="reports")
def task_reports(name, _id, endpoint, method="GET", source='report', params={}, chain=[]):

    query = json.dumps({
        '_id': _id,
        'active': True
    })

    path = FactoryURL.make(path='schedulers')
    resource = requests.post(path, json={'query': query})
    
    if resource.status_code == 200:
        result = resource.json()
        if result.get('found', 0) == 1:
            print(result.get('items')[0].get('link'))
            webhook_id = task_webhook.delay(name, _id, endpoint, source, method, params, chain)
            return {'webhook_id': webhook_id}

        msg = "Report desactived - %s" % _id

    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        msg = resource.text

    #deple_id = task_deplete.delay(msg, _id)
    #return {'deplete_id': deple_id, 'status_code': resource.status_code}
