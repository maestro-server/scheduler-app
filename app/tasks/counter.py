import requests

from app import celery
from app.libs.logger import logger
from app.repository.externalMaestroData import ExternalMaestroData


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

    result = ExternalMaestroData() \
        .put_request(path="schedulers", body=post)

    if result:
        logger.debug("TASK Counter Success")

    return {'statuc_code': result.get_status()}
