
from app.services.maps.trigger_interval_map import TriggerIntervalMap

class TriggerMap(object):

    def __init__(self, data):
        self.__map = {}
        self.__data = data

    def rules(self):
        period_type = self.__data.get('period_type')
        data = self.__data.get(period_type)

        if (period_type == 'interval'):
            data = TriggerIntervalMap(data)\
                .rules()\
                .get_map()

        self.__map = data
        return self

    def get_map(self):
        return self.__map
