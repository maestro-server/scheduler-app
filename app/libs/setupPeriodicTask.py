
from app import celery
from app.repository.scheduler import Scheduler


def setup_periodic():
    Sch = Scheduler()
    data = Sch.getAll()

    for item in data:
        celery.conf.beat_schedule = {
            'add-every-30-seconds': {
                'task': 'scheduler.scan',
                'schedule': int(item['time']),
                'args': (item['name'],)
            },
        }

    Sch.dropConn()