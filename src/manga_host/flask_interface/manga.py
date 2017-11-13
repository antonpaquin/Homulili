import requests
import json
from . import config

url = config.url + '/manga'


def create(name, author, link):
    """
    {
        'id': int,
    }
    """
    params = {key: value for key, value in {
        'name': name,
        'author': author,
        'link': link,
    }.items() if value is not None}

    response = requests.put(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(manga_id):
    params = {key: value for key, value in {
        'id': str(manga_id),
    }.items() if value is not None}

    response = requests.get(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def update(manga_id, name=None, author=None, link=None, active=None):
    params = {key: value for key, value in {
        'id': manga_id,
        'name': name,
        'author': author,
        'link': link,
        'active': active,
    }.items() if value is not None}

    response = requests.patch(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def delete(manga_id):
    params = {key: value for key, value in {
        'id': manga_id,
    }.items() if value is not None}

    response = requests.delete(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def index():
    """
    [
        {
            "id": int,
            "name": str,
        },
    ]
    """
    params = {key: value for key, value in {
    }.items() if value is not None}

    response = requests.request(method='VIEW', url=url, params=params)
    print(response.text)
    print(url)
    print(params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
