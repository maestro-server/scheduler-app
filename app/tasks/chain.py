import requests
import json
from pydash import get, has
from app import celery
from app.libs.url import FactoryURL
from app.tasks.chain_exec import task_chain_exec


@celery.task(name="chain")
def task_chain(id, countdown=0):
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
                task.get('name'),
                task.get('_id'),
                task.get('endpoint'),
                task.get('source', ''),
                task.get('method', 'GET'),
                task.get('args', []),
                task.get('chain', [])]

            task_chain_exec.apply_async((task.get('task'), args), countdown=countdown)

    return {'status_code': result.status_code}
