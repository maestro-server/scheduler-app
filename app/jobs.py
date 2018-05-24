
import datetime
from app.conn import db

class Model(object):
    def __init__(self, collection = "schedulers"):
        print(collection)
        self.col = db[collection]

    def find(self, filter, limit = 100, skip = 0):
        result = self.col.find(filter) \
            .limit(limit) \
            .skip(skip)

        return list(result)

    def findOne(self, filter):
        return self.col.findOne(filter)

    def count(self, filter={}):
        return self.col.count(filter)

class Jobs(Model):

    def delta(self, Timer):
        filter = {'updated_at': {"$gt": Timer.timer()}}
        return self.find(filter)

class Timer(Model):

    def timer(self):
        result = self.findOne({'key': 'time_scheduler'})
        print(result)
