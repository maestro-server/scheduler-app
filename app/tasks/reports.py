
import json
from app import celery

from pydash import from_pairs, map_, pick
from app.libs.transformParams import transformParams
from app.tasks.webhook import task_webhook
from app.tasks.depleted_job import task_deplete
from app.repository.externalMaestroScheduler import ExternalMaestroScheduler

@celery.task(name="reports")
def task_reports(name, _id, endpoint, method="GET", source='report', args={}, chain=[]):
    msg = "Task Report - %s" % _id
    normalize = from_pairs(map_(args, lambda i: [i['key'], i['value']]))

    query = json.dumps({
        '_id': normalize.get('report_id'),
        'owner._id': normalize.get('owner_user'),
        'active': True
    })

    resource = ExternalMaestroScheduler(_id) \
        .post_request(path="reports", body={'query': query})


    if resource.get_status() >= 400:
        msg = resource.get_error()
        task_deplete.delay(msg, _id)

    if resource.get_status() < 400:
        result = resource.get_results()
        msg = "Report success - %s" % _id
        if result.get('found', 0) == 1:
            objs = pick(result.get('items')[0], ['filters', 'component'])
            transformParams(args, objs)
            task_webhook.delay(name, _id, endpoint, source, method, args, chain)


    return {'msg': msg, 'status_code': resource.get_status()}
