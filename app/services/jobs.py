
import json, requests
from urllib.parse import urlencode, quote_plus
from app.libs.logger import logger

from pydash import get
from app.libs.url import FactoryURL
from app.repository.singleton import Singleton

from app.tasks.crawling_job import task_crawling


class Jobs(object, metaclass=Singleton):
    def __init__(self, url="schedulers"):
        self.__jobs = []
        self.__resource = url
        
    def tick(self):
        self.sync_jobs()
        logger.info('Scheduler: Tick[%s] ----> %s', self.__resource, len(self.__jobs))


    def sync_jobs(self):
        query = json.dumps({'crawling': True})

        path = FactoryURL.make(path=self.__resource)
        resource = requests.post(path, json={'query': query})

        if resource.status_code == 200:
            result = resource.json()
            self.__jobs = get(result, 'items', [])
            self.sync_ack()
            
        return self.__jobs

    def sync_ack(self):
        ids = []

        for job in self.__jobs:
            ids.append(get(job, '_id'))

        if len(ids) > 0:
            task_crawling.delay(ids)



    def get_jobs(self):
        return self.__jobs
