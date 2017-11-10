import requests
import json

url = 'http://localhost:8000/chapter'


def create(manga_id, name, sort_key):
    params = {key: value for key, value in {
        'manga_id': manga_id,
        'name': name,
        'sort_key': sort_key,
    }.items() if value is not None}

    response = requests.put(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def read(chapter_id):
    params = {key: value for key, value in {
        'id': chapter_id,
    }.items() if value is not None}

    response = requests.get(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def update(chapter_id, name=None, manga_id=None, sort_key=None):
    params = {key: value for key, value in {
        'id': chapter_id,
        'name': name,
        'manga_id': manga_id,
        'sort_key': sort_key,
    }.items() if value is not None}

    response = requests.patch(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def delete(chapter_id):
    params = {key: value for key, value in {
        'id': chapter_id,
    }.items() if value is not None}

    response = requests.delete(url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def index(manga_id):
    """
    [
        {
            "id": int,
            "name": str,
            "sort_key": int,
        },
    ]
    """
    params = {key: value for key, value in {
        'manga_id': manga_id,
    }.items() if value is not None}

    response = requests.request(method='VIEW', url=url, params=params)

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)


def reorder(chapter_ids):
    params = {key: value for key, value in {
        'command': 'reorder',
    }.items() if value is not None}

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url=url, params=params, headers=headers, data=json.dumps(chapter_ids))

    jsn = json.loads(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        raise RuntimeError(jsn)
