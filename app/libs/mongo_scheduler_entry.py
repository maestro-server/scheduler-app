
import os
import mongoengine
import traceback
import datetime

from pydash import get
from celery.beat import Scheduler, ScheduleEntry
from celery.utils.log import get_logger
from celery import current_app

from app.libs.forceUpdate import ForceUpdate

class MongoScheduleEntry(ScheduleEntry):
    def __init__(self, task):
        self._task = task

        self.app = current_app._get_current_object()
        self.name = self._task.name
        self.task = self._task.task

        self.schedule = self._task.schedule

        self.args = [
                        get(self._task, 'name'),
                        str(get(self._task, 'id')),
                        get(self._task, 'endpoint'),
                        get(self._task, 'method', 'GET'),
                        get(self._task, 'args', []),
                        get(self._task, 'chain', [])]

        self.kwargs = self._task.kwargs
        self.options = {
            'queue': self._task.queue,
            'exchange': self._task.exchange,
            'routing_key': self._task.routing_key,
            'expires': self._task.expires,
            'soft_time_limit': self._task.soft_time_limit
        }
        if self._task.total_run_count is None:
            self._task.total_run_count = 0
        self.total_run_count = self._task.total_run_count

        if not self._task.last_run_at:
            self._task.last_run_at = self._default_now()
        self.last_run_at = self._task.last_run_at


    def _default_now(self):
        return self.app.now()

    def next(self):
        self._task.last_run_at = self.app.now()
        self._task.total_run_count += 1
        self._task.run_immediately = False
        self._task.hit = True
        self._task.no_changes = True

        return self.__class__(self._task)

    __next__ = next

    def is_due(self):
        if not self._task.enabled:
            return False, 5.0  # 5 second delay for re-enable.
        if hasattr(self._task, 'start_after') and self._task.start_after:
            if datetime.datetime.now() < self._task.start_after:
                return False, 5.0
        if hasattr(self._task, 'max_run_count') and self._task.max_run_count:
            if (self._task.total_run_count or 0) >= self._task.max_run_count:
                return False, 5.0

        print(str(self._task.name) + " -------------imm " + str(self._task.run_immediately))
        if self._task.run_immediately:
            return True, 10

        return self.schedule.is_due(self.last_run_at)

    def __repr__(self):
        return (u'<{0} ({1} {2}(*{3}, **{4}) {{5}})>'.format(
            self.__class__.__name__,
            self.name, self.task, self.args,
            self.kwargs, self.schedule,
        ))

    def reserve(self, entry):
        new_entry = Scheduler.reserve(self, entry)
        return new_entry

    def save(self):

        if get(self._task, 'hit', False):
            if self.total_run_count > self._task.total_run_count:
                self._task.total_run_count = self.total_run_count
            if self.last_run_at and self._task.last_run_at and self.last_run_at > self._task.last_run_at:
                self._task.last_run_at = self.last_run_at
            self._task.run_immediately = False
            self._task.hit = False

            self._task.name = ForceUpdate.deserialize(self._task.name)

            print("------------------------------------------>   " + str(self._task.name))
            try:
                res = self._task.save(save_condition={})
            except Exception:
                get_logger(__name__).error(traceback.format_exc())
            except mongoengine.errors.NotUniqueError:
                pass
        pass