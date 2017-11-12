import requests
import json
from . import config

url = config.url + '/pagedata'


def create(page_id, data):
    params = {
        'page_id': page_id,
    }

    response = requests.put(url=url, params=params, data=data)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(page_id):
    params = {
        'page_id': page_id,
    }

    response = requests.get(url=url, params=params)

    return response.content


def delete(page_id):
    params = {
        'page_id': page_id,
    }

    response = requests.delete(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
