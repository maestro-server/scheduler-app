

import random
from pydash import get, pick

from app.libs.logger import logger
from app.repository.singleton import Singleton
from app.services.maps.spawn_map import SpawnMap
from app.tasks import task_connections, task_webhook, task_counter


class SpawnJobs(object, metaclass=Singleton):
    
    def spawn(self, queue, scheduler):
        for spawn in queue:
            id = get(spawn, '_id')

            if id:
                exist = scheduler.get_job(id)
                sjob = self.mapp(spawn)
                if not exist:
                    jobs = self.create(id, scheduler, sjob, SpawnJobs.is_disabled(spawn))
                else:
                    self.update(id, scheduler, sjob, SpawnJobs.is_disabled(spawn))

                if get(spawn, 'run_immediately', False):
                    self.run_now(id, scheduler, sjob, SpawnJobs.is_disabled(spawn))

                logger.info('Scheduler: Spawn Job [%s]', get(spawn, 'name'))

    def create(self, id, scheduler, sjob, removed=False):
        if removed:
            sjob['misfire_grace_time'] = 5
            return scheduler.add_job(SpawnJobs.caller, id=id, **sjob)

    def update(self, id, scheduler, sjob, removed=False):
        scheduler.remove_job(job_id=id)
        return self.create(id, scheduler, sjob, removed)

    def run_now(self, id, scheduler, sjob, removed):
        njob = pick(sjob, ['args'])
        tempid = id + str(random.random() * 100)
        self.create(tempid, scheduler, njob, removed)


    def mapp(self, data):
        return SpawnMap(data)\
            .trigger()\
            .timer()\
            .args()\
            .get_map()

        
    def count(self):
        return len(self.__queue)

    @staticmethod
    def is_disabled(sjob):
        return get(sjob, 'enabled', False) and get(sjob, 'active', False)

    @staticmethod
    def caller(task, args):
        tasks = {'connections': task_connections, 'webhook': task_webhook}

        if task in tasks:
            task_id = tasks[task].delay(**args)
            counter_id = task_counter.delay(_id=get(args, '_id'))
            logger.info('Scheduler: Task executed %s (%s)', task_id, counter_id)
        

