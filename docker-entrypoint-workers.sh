#!/bin/sh

chown -R app:app .
su-exec app celery -A app.celery worker -S app.schedulers.MongoScheduler --loglevel=info
