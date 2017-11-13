import requests
import json
from . import config
from .common import auth_header

url = 'http://{hostname}:{port}/file'.format(
    hostname=config.api_hostname,
    port=config.api_internal_port,
)


def create(manga_id, file_url, location=None, downloaded=False, ignore=False, parsed=False):
    params = {key: value for key, value in {
        'manga_id': manga_id,
        'url': file_url,
        'location': location,
        'downloaded': downloaded,
        'ignore': ignore,
        'parsed': parsed,
    }.items() if value is not None}

    response = requests.put(url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(file_id):
    params = {key: value for key, value in {
        'id': file_id,
    }.items() if value is not None}

    response = requests.get(url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def update(file_id, manga_id=None, file_url=None, location=None, downloaded=None, ignore=None, parsed=None):
    params = {key: value for key, value in {
        'id': file_id,
        'manga_id': manga_id,
        'url': file_url,
        'location': location,
        'downloaded': downloaded,
        'ignore': ignore,
        'parsed': parsed,
    }.items() if value is not None}

    response = requests.patch(url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def delete(file_id):
    params = {key: value for key, value in {
        'id': file_id,
    }.items() if value is not None}

    response = requests.delete(url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def index(manga_id):
    params = {key: value for key, value in {
        'manga_id': manga_id,
    }.items() if value is not None}

    response = requests.request(method='VIEW', url=url, params=params, headers=auth_header)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
