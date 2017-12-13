
import os, requests, json
from app import celery
from app.libs.url import FactoryURL
from urllib.parse import urlencode, quote_plus

from .request import task_request

@celery.task(name="scheduler.scan", bind=True)
def task_scan(self, uri, type, page = 1):

    task_id = None
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
    result = resource.json()

    if 'items' in result:
        task_id = task_request.delay(result['items'], uri)

    if page < result['total_pages']:
        pp = result['page'] + 1
        task_scan.delay(uri, type, pp)

    return {'request_id': task_id}