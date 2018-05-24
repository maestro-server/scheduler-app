from pytz import utc
import asyncio

from app import celery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.libs.jobstore_maestro import MaestroDBJobStore
from app.jobs import Jobs, Timer

if __name__ == '__main__':
    MAESTRO_MONGO_DATABASE = celery.conf["MAESTRO_MONGO_DATABASE"]
    MAESTRO_MONGO_COLLECTION = celery.conf["MAESTRO_MONGO_COLLECTION"]
    MAESTRO_MONGO_URI = celery.conf["MAESTRO_MONGO_URI"]

    jobstores = {
        'default': MaestroDBJobStore(collection=MAESTRO_MONGO_COLLECTION, host=MAESTRO_MONGO_URI, database=MAESTRO_MONGO_DATABASE)
    }

    scheduler = AsyncIOScheduler(timezone=utc, jobstores=jobstores)
    jobs = Jobs(collection=MAESTRO_MONGO_COLLECTION).delta(Timer('adminer'))
    print(jobs)

    scheduler.start()

    print("===> running scheduler")

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass