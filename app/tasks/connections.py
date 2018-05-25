
from app import celery
import re, requests, json
from pydash import get
from urllib.parse import urlencode, quote_plus
from .webhook import task_webhook
from app.libs.url import FactoryURL
from .depleted_job import task_deplete

@celery.task(name="connections")
def task_connections(name, _id, endpoint, method="GET", params={}, chain=[]):

    type = re.search(r'\/[a-zA-Z0-9]{24,24}\/([a-z-]*)$', endpoint).group(1)
    conn_id = re.search(r'\/([a-zA-Z0-9]{24,24})\/', endpoint).group(1)

    process = 'process.%s.state' % type
    query = json.dumps({
        '_id': conn_id,
        'status': 'enabled',
        'active': True,
        process: {'$ne': 'danger'}
    })

    post = urlencode({'query': query}, quote_via=quote_plus)
    path = FactoryURL.make(path="connections")
    resource = requests.post(path, json={'query': query})

    if resource.status_code == 200:
        result = resource.json()
        if get(result, 'found', 0) == 1:
            webhook_id = task_webhook.delay(name, _id, endpoint, method, params, chain)
            return {'webhook_id': webhook_id}

        msg = "Empty results - %s" % conn_id

    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        msg = resource.text

    deple_id = task_deplete.delay(msg, _id)
    return {'deplete_id': deple_id, 'status_code': resource.status_code}