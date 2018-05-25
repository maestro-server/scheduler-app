
from app.libs.conn import db

class Model(object):
    def __init__(self, collection = "schedulers"):
        self.col = db[collection]

    def update(self, filter, data):
        self.col.update_one(filter, {"$set": data}, upsert=True)

    def find(self, filter, limit = 100, skip = 0):
        result = self.col.find(filter) \
            .limit(limit) \
            .skip(skip)

        return list(result)

    def findOne(self, filter):
        return self.col.find_one(filter)

    def count(self, filter={}):
        return self.col.count(filter)
