
import os
import json
from pydash import pick


def appInfo():
    base = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(base, '../../')

    file = open(root_path + '/package.json')
    json_data = file.read()
    data = json.loads(json_data)

    file.close()
    return pick(data, ['name', 'provider', 'description', 'version', 'license'])