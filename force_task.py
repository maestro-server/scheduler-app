from app.tasks import task_scan

task_scan.delay('server-list')