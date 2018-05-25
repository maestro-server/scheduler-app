
import json, requests
from urllib.parse import urlencode, quote_plus
from app.libs.logger import logger

from pydash import get
from app.libs.url import FactoryURL
from app.repository.singleton import Singleton


class Jobs(object, metaclass=Singleton):
    def __init__(self, timer, url = "schedulers"):
        self.__jobs = []
        self.__timer = timer
        self.__resource = url
        
    def tick(self):
        rule = self.__timer.timer()
        self.__timer.updateTime()
        self.sync_jobs(rule)
        logger.info('Tick[%s] ----> %s', self.__resource, len(self.__jobs))


    def sync_jobs(self, rule):
        query = json.dumps({'updated_at': {"$gt": rule.isoformat()}})

        post = urlencode({'query': query}, quote_via=quote_plus)
        path = FactoryURL.make(path=self.__resource)
        resource = requests.post(path, json={'query': query})

        if resource.status_code == 200:
            result = resource.json()
            self.__jobs = get(result, 'items', [])
            
        return self.__jobs

    def get_jobs(self):
        return self.__jobs
