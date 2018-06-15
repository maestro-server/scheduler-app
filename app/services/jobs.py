import json
import requests
from app.libs.logger import logger
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

        try:
            path = FactoryURL.make(path=self.__resource)
            resource = requests.post(path, json={'query': query})
        except requests.exceptions.ConnectionError as error:
            return logger.error("Scheduler: Data Layer is down [%s]", str(error))

        if resource.status_code == 200:
            result = resource.json()
            self.__jobs = result.get('items', [])
            self.sync_ack()

        return self.__jobs

    def sync_ack(self):
        ids = []

        for job in self.__jobs:
            ids.append(job.get('_id'))

        if len(ids) > 0:
            task_crawling.delay(ids)

    def get_jobs(self):
        return self.__jobs
