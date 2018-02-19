
import os, requests, json
from app import celery
from app.libs.url import FactoryURL
from urllib.parse import urlencode, quote_plus

from .notify_event import task_notify_event
from .request import task_request

@celery.task(name="scheduler.scan")
def task_scan(type, page=1):

    task_id = []
    process = 'process.%s.state' % type
    query = json.dumps({
        'status': 'enabled',
        'active': True,
        process: {'$ne': 'danger'}
    })

    params = {
        'query': query,
        'limit': os.environ.get("MAESTRO_SCAN_QTD", 50),
        'page': page
    }

    url_values = urlencode(params, quote_via=quote_plus)
    path = FactoryURL.make(path="connections?%s" % url_values)
    resource = requests.get(path)

    if resource.status_code == 200:
        result = resource.json()

        if 'items' in result:
            for item in result['items']:
                tid = task_request.delay(item, type)
                task_id.append(str(tid))

        if page < result['total_pages']:
            pp = result['page'] + 1
            task_scan.delay(type, pp)

        return {'type': type, 'count': len(task_id), 'task_id': task_id}


    if resource.status_code in [400, 403, 404, 500, 501, 502, 503]:
        return {'type': type, 'err': resource.text}, resource.status_code


