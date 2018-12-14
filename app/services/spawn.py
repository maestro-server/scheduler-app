
import random
from pydash import pick
from app.libs.logger import logger
from app.repository.singleton import Singleton
from app.services.maps.spawn_map import SpawnMap
from app.tasks import task_connections, task_webhook, task_counter, task_reports


class SpawnJobs(object, metaclass=Singleton):

    def spawn(self, queue, scheduler):
        for spawn in queue:
            spawnId = spawn.get('_id')

            if spawnId:
                exist = scheduler.get_job(spawnId)
                sjob = SpawnJobs.mapp(spawn)
                if not exist:
                    jobs = self.create(spawnId, scheduler, sjob, SpawnJobs.is_disabled(spawn))
                    logger.info('Scheduler: Create Job [%s]', str(jobs))
                else:
                    self.update(spawnId, scheduler, sjob, SpawnJobs.is_disabled(spawn))
                    logger.info('Scheduler: Update Job [%s]', spawnId)

                if spawn.get('run_immediately', False):
                    self.run_now(spawnId, scheduler, sjob, SpawnJobs.is_disabled(spawn))
                    logger.info('--------------->>>>>> Scheduler: Run immediaty [%s]', spawn.get('name'))

                logger.info('Scheduler: Crawler Job [%s]', spawn.get('name'))

    def create(self, jobId, scheduler, sjob, removed=False):
        if removed:
            sjob['misfire_grace_time'] = 15
            return scheduler.add_job(SpawnJobs.caller, id=jobId, **sjob)

    def update(self, jobId, scheduler, sjob, removed=False):
        scheduler.remove_job(job_id=jobId)
        return self.create(jobId, scheduler, sjob, removed)

    def run_now(self, jobId, scheduler, sjob, removed):
        njob = pick(sjob, ['args'])
        tempid = jobId + str(random.random() * 100)
        self.create(tempid, scheduler, njob, removed)

    def count(self):
        return len(self.__queue)

    def mapp(data):
        return SpawnMap(data)\
            .trigger()\
            .timer()\
            .args()\
            .get_map()

    @staticmethod
    def is_disabled(sjob):
        return sjob.get('enabled', False) and sjob.get('active', False)

    @staticmethod
    def caller(task, args):
        tasks = {'connections': task_connections, 'webhook': task_webhook, 'reports': task_reports}

        if task in tasks:
            
            task_id = tasks[task].delay(**args)
            counter_id = task_counter.delay(_id=args.get('_id'))
            logger.info('Scheduler: Task executed %s (%s)', task_id, counter_id)