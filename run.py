from pytz import utc
import asyncio

from app import celery
from app.services.jobs import Jobs
from app.services.spawn import SpawnJobs
from app.libs.timer import Timer
from app.libs.logger import logger
from app.repository.jobstore.default import jobstores
from apscheduler.schedulers.asyncio import AsyncIOScheduler


if __name__ == '__main__':
    collection = celery.conf["MAESTRO_MONGO_COLLECTION"]
    loop_time = celery.conf["MAESTRO_LOOP_TIME"]

    scheduler = AsyncIOScheduler(timezone=utc, jobstores=jobstores)
    Jobber = Jobs(timer=Timer('adminer'), collection=collection)

    def warmup():
        Jobber.tick()
        jobs = Jobber.get_jobs()
        SpawnJobs(jobs).spawn(scheduler)
    
    scheduler.add_job(warmup, 'interval', seconds=loop_time)

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass