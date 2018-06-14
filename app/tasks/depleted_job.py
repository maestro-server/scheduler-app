from app import celery
from app.libs.url import FactoryURL
from app.libs.data_request import data_request


@celery.task(name="deplete")
def task_deplete(msg, job_id):
    path = FactoryURL.make(path="schedulers")

    post = {
        'body': [{
            '_id': job_id,
            'msg': msg,
            'crawling': True,
            'enabled': False
        }]
    }

    return data_request(path, post)
