
import pymongo
from app.libs.logger import logger
from pymongo import MongoClient
from app import celery

client = MongoClient(celery.conf['MAESTRO_MONGO_URI'], serverSelectionTimeoutMS=1)
db = client[celery.conf['MAESTRO_MONGO_DATABASE']]

try:
    client.server_info()  # Forces a call.
    logger.info("Mongo Online")
except pymongo.errors.ServerSelectionTimeoutError as err:
    logger.error("MongoDB is down [%s]", err)