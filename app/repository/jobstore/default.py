from app import celery
from apscheduler.jobstores.mongodb import MongoDBJobStore

MAESTRO_MONGO_DATABASE = celery.conf["MAESTRO_MONGO_DATABASE"]
MAESTRO_MONGO_COLLECTION = celery.conf["MAESTRO_MONGO_COLLECTION"]
MAESTRO_MONGO_URI = celery.conf["MAESTRO_MONGO_URI"]
MAESTRO_LOOP_TIME = celery.conf["MAESTRO_LOOP_TIME"]

jobstores = {
    'default': MongoDBJobStore(collection=MAESTRO_MONGO_COLLECTION, host=MAESTRO_MONGO_URI, database=MAESTRO_MONGO_DATABASE)
}