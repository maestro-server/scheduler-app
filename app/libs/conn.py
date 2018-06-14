import pymongo
from app import celery
from pymongo import MongoClient
from app.libs.logger import logger

client = MongoClient(
                    celery.conf['MAESTRO_MONGO_URI'], 
                    serverSelectionTimeoutMS=1)
                    
db = client[celery.conf['MAESTRO_MONGO_DATABASE']]

try:
    client.server_info()  # Forces a call.
    logger.info("Scheduler: Mongo Online")
except pymongo.errors.ServerSelectionTimeoutError as err:
    logger.error("Scheduler: MongoDB is down [%s]", str(err))
