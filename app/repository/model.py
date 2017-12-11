
import datetime
from app.libs.connection import DBConection
from bson.objectid import ObjectId
from app.error.missingError import MissingError


class Model(object):

    __conn = None

    def __init__(self, id=None):
        name = self.__class__.__name__.lower()
        db = self.setupConn()
        self.col = db[name]
        self.__id = id

    def setupConn(self):
        print("setup ==============================")
        self.__conn = DBConection()
        return self.__conn.conn_up()

    def dropConn(self):
        print("downn ==============================")
        return self.__conn.conn_down()


    def getAll(self, filter = {}, limit = 10, skip = 0):
        result = self.col.find(filter)\
            .limit(limit)\
            .skip(skip)

        return list(result)

    def count(self, filter = {}):
        return self.col.count(filter)

    def get(self):
        return self.col.find_one(Model.makeObjectId(self.__id))

    def update(self, data):
        if not self.__id:
            raise MissingError('id', 'Id not setted')

        set = {'$set': data}
        result = self.col.update_one(Model.makeObjectId(self.__id), set)
        return result.raw_result


    def makeDateAt(self, key):
        return {key: datetime.datetime.utcnow()}

    @staticmethod
    def makeObjectId(id):
        if id:
            return {'_id': Model.castObjectId(id)}

    @staticmethod
    def castObjectId(id):
        return ObjectId(id)