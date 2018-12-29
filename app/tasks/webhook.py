import requests
from pydash import from_pairs, map_

from app import celery
from app.tasks.notify_event import task_notify_event
from app.tasks.depleted_job import task_deplete
from app.tasks.chain import task_chain
from app.services.privateAuth.decorators.external_private_token import create_jwt
from app.repository.externalMaestroScheduler import ExternalMaestroScheduler


def call_chains(chain):
    if chain:
        for job in chain:
            task_chain.delay(job.get('_id'), job.get('countdown'))


@celery.task(name="webhook")
def task_webhook(name, _id, endpoint, source=None, method="GET", args={}, chain=[]):
    normalize = from_pairs(map_(args, lambda i: [i['key'], i['value']]))
    msg = "Scheduler run - %s" % (name)

    EREquester = ExternalMaestroScheduler(_id, source) \
        .set_headers(create_jwt())

    try:
        funcm = "%s_request" % method.lower()
        result = getattr(EREquester, funcm)(path=endpoint, body=normalize)\
            .get_results()

    except requests.exceptions.RequestException as error:
        deple_id = task_deplete.delay(str(error), _id)
        return {'msg': result, 'deple_id': deple_id}

    if result:
        notify_id = task_notify_event.delay(msg=msg, roles=EREquester.templateRoles(), description=result, status='success')
        call_chains(chain)

        return {'notify_id': notify_id}
