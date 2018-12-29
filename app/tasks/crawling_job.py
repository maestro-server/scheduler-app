from app import celery
from app.repository.externalMaestroData import ExternalMaestroData


@celery.task(name="crawling")
def task_crawling(ids):

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

        return ExternalMaestroData() \
            .put_request(path="schedulers", body=post) \
            .get_results()
