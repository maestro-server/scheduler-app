import re
import requests
import json

from app import celery

from app.libs.url import FactoryURL
from app.tasks.webhook import task_webhook
from app.tasks.depleted_job import task_deplete


@celery.task(name="reports")
def task_reports(name, _id, endpoint, method="GET", args=[], params={}, chain=[]):
    print(name, _id, endpoint, method, args, params, chain)
    query = json.dumps({
        '_id': _id,
        'active': True
    })

    path = FactoryURL.make(path="reports")
    resource = requests.post(path, json={'query': query})


    return {_id}
