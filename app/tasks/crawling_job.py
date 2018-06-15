from app import celery
from app.libs.url import FactoryURL
from app.libs.data_request import data_request


@celery.task(name="crawling")
def task_crawling(ids):
    path = FactoryURL.make(path="schedulers")

    body = []
    for id in ids:
        if id:
            body.append({
                '_id': id,
                '$unset': {'crawling': True, 'run_immediately': True}
            })

    if len(body) > 0:
        post = {
            'body': body
        }

        return data_request(path, post)
