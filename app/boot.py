
from datetime import datetime, timedelta
import sys
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    import asyncio
except ImportError:
    import trollius as asyncio


def alarm(time):
    pass
    print('Alarm! This alarm was scheduled at %s.' % datetime.now())


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_jobstore('mongodb', collection='example_jobs', host='localhost')
    scheduler.start()

    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        scheduler.remove_all_jobs()

    alarm_time = datetime.now() + timedelta(seconds=10)

    scheduler.add_job(alarm, 'interval', seconds=5, args=[datetime.now()])
    print('To clear the alarms, run this example with the --clear argument.')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    scheduler.lookup_job('7c9c459dc9bf4606bcc8116354413e4a')


    print("==", repr(scheduler.get_jobs()))
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass