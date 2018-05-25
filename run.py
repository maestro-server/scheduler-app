from pytz import utc
import asyncio

from app import celery
from app.services.jobs import Jobs
from app.services.spawn import SpawnJobs
from app.libs.timer import Timer
from app.libs.logger import logger
from app.repository.jobstore.default import jobstores
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

from datetime import datetime, timedelta

if __name__ == '__main__':
    collectio_timer = celery.conf["MAESTRO_MONGO_COLLECTION_TIMER"]
    loop_time = celery.conf["MAESTRO_LOOP_TIME"]

    scheduler = AsyncIOScheduler(timezone=utc, jobstores=jobstores)
    Jobber = Jobs(timer=Timer(collectio_timer))

    def warmup():
        Jobber.tick()
        jobs = Jobber.get_jobs()
        SpawnJobs().spawn(jobs, scheduler) 
    
    scheduler.start()

    warmjob = scheduler.get_job("warmup")
    if not warmjob:
        scheduler.add_job(warmup, trigger='interval', seconds = loop_time, id="warmup")
    else:
        scheduler.reschedule_job(trigger='interval', seconds = loop_time, job_id="warmup")
        pass   

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass