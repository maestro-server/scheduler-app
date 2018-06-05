import requests

from app import celery
from app.libs.logger import logger
from app.libs.url import FactoryURL


@celery.task(name="counter")
def task_counter(_id):
    if not _id:
        logger.error("Scheduler: [TASK Counter] Missing ID", _id)
        return

    post = {
        'body': [{
            '_id': _id,
            '$inc': {'total_run_count': 1}
        }]
    }

    path = FactoryURL.make(path="schedulers")
    result = requests.put(path, json=post)

    if result.status_code in [200, 201, 204]:
        logger.debug("TASK Counter Success")

    if result.status_code in [400, 403, 404, 500, 501, 502, 503]:
        msg = "ERROR %s" % str(result.text)
        logger.error("Scheduler: [TASK Counter] %s", msg)

    return {'statuc_code': result.status_code}
