import requests
import json
from . import config
from .common import auth_header


url = 'http://{hostname}:{port}/pagedata'.format(
    hostname=config.api_hostname,
    port=config.api_public_port,
)


def create(page_id, data):
    params = {
        'page_id': page_id,
    }

    response = requests.put(url=url, params=params, data=data, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(page_id):
    params = {
        'page_id': page_id,
    }

    response = requests.get(url=url, params=params, headers=auth_header)

    return response.content


def delete(page_id):
    params = {
        'page_id': page_id,
    }

    response = requests.delete(url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
