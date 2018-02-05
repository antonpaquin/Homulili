import requests
import logging
import json

import config

url = 'http://{hostname}:{port}/'.format(
    hostname=config.cdn_hostname,
    port=config.cdn_public_port,
)


def upload(data):
    resp = requests.post(
        url=url,
        data=data,
    )
    data = json.loads(resp.text)
    return data['new_id']


def image(img_id):
    resp = requests.get(url=url + str(img_id))
    return resp.content
