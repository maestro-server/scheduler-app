

from pydash import get, has, pick
from app.libs.logger import logger
from app.repository.singleton import Singleton

from app.tasks import task_connections, task_webhook


class SpawnJobs(object, metaclass=Singleton):
    
    def spawn(self, queue, scheduler):
        for spawn in queue:
            id = get(spawn, '_id')

            exist = scheduler.get_job(id)
            sjob = self.mapp(spawn)
            if not exist:
                jobs = self.create(id, scheduler, sjob, SpawnJobs.is_disabled(spawn))
            else:
                self.update(id, scheduler, sjob, SpawnJobs.is_disabled(spawn))
        
            logger.info('Spawn Job [%s]', get(spawn, 'name'))

    def create(self, id, scheduler, sjob, removed=False):
        if removed:
            return scheduler.add_job(SpawnJobs.caller, id=id, **sjob)

    def update(self, id, scheduler, sjob, removed=False):
        scheduler.remove_job(job_id=id)
        return self.create(id, scheduler, sjob, removed)

    def mapp(self, data):
        timer = get(data, 'timer', {})

        return {
            'trigger': get(data, 'period_type', 'date'),
            'args': [get(data, 'task', 'webhook'), pick(data, ['name', '_id', 'endpoint', 'method', 'params', 'chain'])],
            **timer
        }
        
    def count(self):
        return len(self.__queue)

    @staticmethod
    def is_disabled(sjob):
        return  get(sjob, 'enabled', False) and get(sjob, 'active', False)

    @staticmethod
    def caller(task, args):
        tasks = {'connections': task_connections, 'webhook': task_webhook}

        if task in tasks:
            task_id = tasks[task].delay(**args)
            logger.info('task executed %s', task_id)
        

