from pytz import utc
import asyncio

from app import celery
from app.services.jobs import Jobs
from app.services.spawn import SpawnJobs
from app.repository.jobstore.default import jobstores
from apscheduler.schedulers.asyncio import AsyncIOScheduler

if __name__ == '__main__':
    loop_time = celery.conf["MAESTRO_LOOP_TIME"]

    scheduler = AsyncIOScheduler(timezone=utc, jobstores=jobstores, misfire_grace_time=15)
    Jobber = Jobs()


    def warmup():
        Jobber.tick()
        jobs = Jobber.get_jobs()
        SpawnJobs().spawn(jobs, scheduler)


    scheduler.start()

    warmjob = scheduler.get_job("warmup")
    if not warmjob:
        scheduler.add_job(warmup, trigger='interval', seconds=loop_time, id="warmup")
    else:
        scheduler.reschedule_job(trigger='interval', seconds=loop_time, job_id="warmup")
        pass

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
