
import requests, json
from pydash import get, has
from app import celery
from app.libs.url import FactoryURL

from .chain_exec import task_chain_exec

@celery.task(name="chain")
def task_chain(id, countdown = 0):
    post = json.dumps({
        '_id': id,
        'enabled': True,
        'active': True
    })

    path = FactoryURL.make(path="schedulers")
    result = requests.post(path, json={'query': post})

    if result.status_code == 200:
        task = get(result.json(), 'items[0]')

        if has(task, 'task'):
            args = [
                        get(task, 'name'),
                        get(task, '_id'),
                        get(task, 'endpoint'),
                        get(task, 'method', 'GET'),
                        get(task, 'args', []),
                        get(task, 'chain', [])]

            task_chain_exec.apply_async((get(task, 'task'), args), countdown=countdown)

    return {'status_code': result.status_code}