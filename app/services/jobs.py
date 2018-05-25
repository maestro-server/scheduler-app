

from app.libs.logger import logger

from app.libs.timer import Timer
from app.repository.models import Model
from app.repository.singleton import Singleton


class Jobs(Model, metaclass=Singleton):
    def __init__(self, timer, collection = "schedulers"):
        self.__jobs = []
        self.__timer = timer
        super().__init__(collection)
        
    def tick(self):
        rule = self.__timer.timer()
        self.__timer.updateTime()
        self.__jobs = self.find({'updated_at': {"$gt": rule}})
        logger.info('Tick[%s] ----> %s', self.col.name, len(self.__jobs))

    def get_jobs(self):
        return self.__jobs

