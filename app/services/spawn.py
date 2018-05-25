

from app.libs.logger import logger
from app.repository.singleton import Singleton


class SpawnJobs(object, metaclass=Singleton):
    
    def __init__(self, jobs):
        self.__jobs = jobs
        
    def spawn(self, scheduler):
        print(scheduler.get_jobs())
        name = "tester"
        logger.info('Spawn Job [%s]', name)

