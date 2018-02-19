from celery import Celery
from app.repository.scheduler import Scheduler

celery = Celery('scheduler_maestro')
celery.config_from_object('instance.config.Config')

import app.tasks

beats = {}
Sch = Scheduler()
data = Sch.getAll()

for item in data:
    beats[item['name']] = {
        'task': 'scheduler.scan',
        'schedule': int(item['time']),
        'args': (item['name'],)
    }

Sch.dropConn()
celery.conf.beat_schedule = beats
