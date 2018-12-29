
from instance.config import Config
from app.libs.logger import logger
from .externalMaestro import ExternalMaestro
from app.tasks.notify_event import task_notify_event
from app.services.privateAuth.decorators.external_private_token import add_external_header_auth

@add_external_header_auth
class ExternalMaestroScheduler(ExternalMaestro):
    
    def __init__(self, entity_id=None, source='data'):
        base = self.getConfig(source)
        self.ent_id = entity_id
        super().__init__(base)

        self.private_auth_header()

    def getConfig(self, service):
        if service:
            upper = service.upper()
            vars = "MAESTRO_%s_URI" % upper

            return getattr(Config, vars)

        return ''

    def templateRoles(self):
        return [{
            "_id": self.ent_id,
            "refs": "scheduler",
            "role": 5
        }]

    def error_handling(self, task='', msg=''):
        logger.error("MaestroData:  [%s] - %s", task, msg)
        task_notify_event.delay(msg=msg, roles=self.templateRoles(), description=msg, status='danger')