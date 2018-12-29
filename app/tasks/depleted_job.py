
from app import celery
from app.repository.externalMaestroData import ExternalMaestroData


@celery.task(name="deplete")
def task_deplete(msg, job_id):

    body = {
        'body': [{
            '_id': job_id,
            'msg': msg,
            'crawling': True,
            'enabled': False
        }]
    }

    return ExternalMaestroData() \
        .put_request(path="schedulers", body=body) \
        .get_results()
