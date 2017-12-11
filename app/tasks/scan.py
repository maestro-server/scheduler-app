
import os
from app import celery
from app.repository import Connections

@celery.task(name="scheduler.scan", bind=True)
def task_scan(self, uri, type, skip = 0):

    limit = os.environ.get("MAESTRO_SCAN_QTD", 400)
    filter = {
        'status': 'enabled',
        'active': True,
        'process.server-list.state': {'$ne': 'danger'}
    }

    Conn = Connections()

    result = {
        'found': Conn.count(filter),
        'limit': limit,
        'skip': skip,
        'items': Conn.getAll(filter, limit, skip)
    }
    print("ok", result)

    Conn.dropConn()
    return result