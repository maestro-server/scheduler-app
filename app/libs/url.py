import os
from instance.config import Config

class FactoryURL(object):

    @staticmethod
    def discovery(path):
        if path:
            upper = path.upper()
            vars = "MAESTRO_%s_URI" % upper
            return getattr(Config, vars)
        return ''

    @staticmethod
    def make(path=""):
        base = getattr(Config, "MAESTRO_DATA_URI")
        return "%s/%s" % (base, path)
