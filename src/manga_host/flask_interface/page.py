import requests
import json
from . import config

url = config.url + '/page'


def create(chapter_id, sort_key, file):
    params = {key: value for key, value in {
        'chapter_id': chapter_id,
        'sort_key': sort_key,
        'file': file,
    }.items() if value is not None}

    response = requests.put(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(page_id):
    params = {key: value for key, value in {
        'id': page_id,
    }.items() if value is not None}

    response = requests.get(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def update(page_id, chapter_id=None, sort_key=None, file=None):
    params = {key: value for key, value in {
        'id': page_id,
        'chapter_id': chapter_id,
        'sort_key': sort_key,
        'file': file
    }.items() if value is not None}

    response = requests.patch(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def delete(page_id):
    params = {key: value for key, value in {
        'id': page_id,
    }.items() if value is not None}

    response = requests.delete(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def index(chapter_id):
    """
    [
        {
            'id': int,
            'sort_key': int,
        },
    ]
    """
    params = {key: value for key, value in {
        'chapter_id': chapter_id,
    }.items() if value is not None}

    response = requests.request(method='VIEW', url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
