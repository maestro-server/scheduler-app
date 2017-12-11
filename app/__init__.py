from celery import Celery

celery = Celery('scheduler_maestro')
celery.config_from_object('instance.config.Config')

import app.tasks

app.tasks.scan.task_scan.delay('/crawler/<provider>/<instance_id>/<job>', 'servers-list')