import os
import requests

def data_request(path, post):
    try:
        resource = requests.put(path, json=post)
        return {'status_code': resource.status_code}
    except Exception as error:
        return {'error': str(error)}
