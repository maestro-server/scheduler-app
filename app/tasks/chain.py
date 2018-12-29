
import json
from pydash import has
from app import celery
from app.tasks.chain_exec import task_chain_exec
from app.repository.externalMaestroScheduler import ExternalMaestroScheduler

@celery.task(name="chain")
def task_chain(id, countdown=0):
    post = json.dumps({
        '_id': id,
        'enabled': True,
        'active': True
    })

    result = ExternalMaestroScheduler(id) \
        .post_request(path="schedulers", body={'query': post}) \
        .get_results('items')

    if result:
        task = result[0]
        if has(task, 'task'):
            args = [
                task.get('name'),
                task.get('_id'),
                task.get('endpoint'),
                task.get('source', ''),
                task.get('method', 'GET'),
                task.get('args', []),
                task.get('chain', [])]

            task_chain_exec.apply_async((task.get('task'), args), countdown=countdown)

    return {'id': id}
