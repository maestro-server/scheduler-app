#!/bin/sh

chown -R app:app .
rm -f celerybeat.pid
su-exec app celery -A app.celery beat -S app.schedulers.MongoScheduler --loglevel=info