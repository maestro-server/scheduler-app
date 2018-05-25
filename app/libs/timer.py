
import datetime
from pydash import get
from datetime import timedelta
from app.repository.singleton import Singleton
from app.repository.models import Model

class Timer(Model, metaclass=Singleton):
    
    __filter = {'key': 'time_scheduler'}

    def timer(self):
        result = self.findOne(self.__filter)
        default = self.getNow() - timedelta(days=60)
        return get(result, 'warmup', default)

    def updateTime(self):
        datet = {'warmup': self.getNow()}
        return self.update(self.__filter, datet)

    def getNow(self):
        return datetime.datetime.now()
