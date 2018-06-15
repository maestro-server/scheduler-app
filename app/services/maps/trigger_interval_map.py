
class TriggerIntervalMap(object):

    def __init__(self, data):
        self.__map = {}
        self.__data = data

    def rules(self):
        period = self.__data.get('period')
        time = self.__data.get('every')

        self.__map = {period: time}
        return self

    def get_map(self):
        return self.__map
