import requests
import logging
import json

import config

url = 'http://{hostname}:{port}/'.format(
    hostname=config.cdn_hostname,
    port=config.cdn_public_port,
)

logger = logging.getLogger(__name__)


def upload(data):
    logger.info('imgdata::upload')
    logger.debug('Sending file')
    resp = requests.post(
        url=url + 'upload',
        data=data,
    )

    resp_data = json.loads(resp.text)
    new_id = resp_data['new_id']
    logger.debug('Got fileno {fnum}'.format(
        fnum=new_id,
    ))
    return new_id


def image(img_id):
    logger.info('imgdata::get')
    resp = requests.get(url=url + str(img_id))
    return resp.content
