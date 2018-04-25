# Copyright 2013 Regents of the University of Michigan

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0

import mongoengine
import datetime

from celery.beat import Scheduler
from app.libs.mongo_scheduler_entry import MongoScheduleEntry
from app.libs.forceUpdate import ForceUpdate
from app.repository.models import PeriodicTask
from celery.utils.log import get_logger
from celery import current_app


class MongoScheduler(Scheduler):
    #: how often should we sync in schedule information
    #: from the backend mongo database
    UPDATE_INTERVAL = datetime.timedelta(seconds=5)

    Entry = MongoScheduleEntry

    Model = PeriodicTask

    def __init__(self, *args, **kwargs):
        if hasattr(current_app.conf, "MAESTRO_MONGO_DATABASE"):
            db = current_app.conf.MAESTRO_MONGO_DATABASE
        else:
            db = "celery"
        if hasattr(current_app.conf, "MAESTRO_MONGO_URI"):
            self._mongo = mongoengine.connect(db, host=current_app.conf.MAESTRO_MONGO_URI)
            get_logger(__name__).info("backend scheduler using %s/%s:%s",
                                      current_app.conf.MAESTRO_MONGO_URI,
                                      db, self.Model._get_collection().name)
        else:
            self._mongo = mongoengine.connect(db)
            get_logger(__name__).info("backend scheduler using %s/%s:%s",
                                      "mongodb://localhost",
                                      db, self.Model._get_collection().name)

        self._schedule = {}
        self._last_updated = None
        Scheduler.__init__(self, *args, **kwargs)
        self.max_interval = (kwargs.get('max_interval')
                             or self.app.conf.CELERYBEAT_MAX_LOOP_INTERVAL or 5)

    def setup_schedule(self):
        pass

    def requires_update(self):
        """check whether we should pull an updated schedule
        from the backend database"""
        if not self._last_updated:
            return True
        return self._last_updated + self.UPDATE_INTERVAL < datetime.datetime.now()

    def get_from_database(self):
        self.sync()
        d = {}
        for doc in self.Model.objects(enabled=True, active=True):
            doc.name = ForceUpdate.serialize(doc)
            d[doc.name] = self.Entry(doc)
        return d

    @property
    def schedule(self):
        if self.requires_update():
            self._schedule = self.get_from_database()
            self._last_updated = datetime.datetime.now()
        return self._schedule

    def sync(self):
        for entry in self._schedule.values():
            try:
                entry.save()
            except mongoengine.errors.NotUniqueError:
                pass
