
import pymongo
from pymongo import MongoClient
from instance.config import Config

class DBConection():

    __db = None
    __client = None

    def get_conn(self):
        return self.__db

    def conn_up(self):
        self.__client = MongoClient(Config.DATABASE_URI, serverSelectionTimeoutMS=1)
        self.__db = self.__client[Config.DATABASE_NAME]

        try:
            self.__client.server_info()  # Forces a call.
            print("Mongo Online")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print("==================================> MongoDB is down", err)

        return self.get_conn()

    def conn_down(self):
        if self.__client:
            return self.__client.close()