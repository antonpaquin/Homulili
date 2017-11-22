import logging
import requests

from . import config
from .common import standard_request, auth_header

logger = logging.getLogger(__name__)

url = 'http://{hostname}:{port}/pagedata'.format(
    hostname=config.api_hostname,
    port=config.api_public_port,
)


def create(page_id, data):
    return standard_request(
        model='pagedata',
        method='create',
        params={
            'page_id': page_id,
        },
        logger=logger,
    )


def read(page_id):
    params = {
        'page_id': page_id,
    }

    response = requests.get(url=url, params=params, headers=auth_header)

    return response.content


def delete(page_id):
    return standard_request(
        model='pagedata',
        method='delete',
        params={
            'page_id': page_id,
        },
        logger=logger,
    )
