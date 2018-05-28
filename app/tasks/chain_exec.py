from app import celery


@celery.task(name="chain_exec")
def task_chain_exec(task, args):
    import app.tasks.webhook as module_webhook
    import app.tasks.connections as module_connections

    tasks = {
        'connections': module_connections.task_connections,
        'webhook': module_webhook.task_webhook
    }

    if task in tasks:
        tasks[task].delay(*args)

    return {'post': args}
