import os
from instance.config import Config

class FactoryURL(object):

    @staticmethod
    def discovery(service):
        if service:
            upper = service.upper()
            vars = "MAESTRO_%s_URI" % upper
            return getattr(Config, vars)
        return ''

    @staticmethod
    def make(path="", service='Data'):
        base = FactoryURL.discovery(service)
        return "%s/%s" % (base, path)
