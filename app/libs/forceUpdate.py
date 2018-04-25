
import re

class ForceUpdate(object):

    @staticmethod
    def serialize(doc):
        return "%s [[%s]]" % (doc.name, doc.updated_at.timestamp())

    @staticmethod
    def deserialize(doc):
        normalize = re.sub(r'\[\[([0-9\.]*)\]\]$', '', doc)
        return normalize.strip()