
from instance.config import Config
from .externalMaestro import ExternalMaestro

from app.services.privateAuth.decorators.external_private_token import add_external_header_auth

@add_external_header_auth
class ExternalMaestroData(ExternalMaestro):
    
    def __init__(self):
        base = Config.MAESTRO_DATA_URI
        super().__init__(base)

        self.private_auth_header()