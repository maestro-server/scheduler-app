
import pymongo
from pymongo import MongoClient
from app import celery

client = MongoClient(celery.conf['MAESTRO_MONGO_URI'], serverSelectionTimeoutMS=1)
db = client[celery.conf['MAESTRO_MONGO_DATABASE']]

try:
    client.server_info()  # Forces a call.
    print("Mongo Online")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print("==================================> MongoDB is down", err)