

from pydash import pick
from app.services.maps.trigger_map import TriggerMap


class SpawnMap(object):

    def __init__(self, data):
        self.__map = {}
        self.__data = data

    def timer(self):
        timer = TriggerMap(self.__data)\
            .rules()\
            .get_map()

        self.__map.update(timer)
        return self

    def trigger(self):
        obj = {'trigger': self.__data.get('period_type', 'date')}
        self.__map.update(obj)
        return self

    def args(self):
        obj = {'args': [self.__data.get('task', 'webhook'), pick(self.__data, ['name', '_id', 'endpoint', 'method', 'params', 'chain'])]}
        self.__map.update(obj)
        return self

    def get_map(self):
        return self.__map
        