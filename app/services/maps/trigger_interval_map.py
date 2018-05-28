
from pydash import get

class TriggerIntervalMap(object):

    def __init__(self, data):
        self.__map = {}
        self.__data = data

    def rules(self):
        period = get(self.__data, 'period')
        time = get(self.__data, 'every')

        self.__map = {period: time}
        return self

    def get_map(self):
        return self.__map
