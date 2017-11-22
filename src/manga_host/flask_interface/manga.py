import logging

from .common import standard_request

logger = logging.getLogger(__name__)


def create(name, author, link):
    """
    {
        'id': int,
    }
    """
    return standard_request(
        model='manga',
        method='create',
        params={
            'name': name,
            'author': author,
            'link': link,
        },
        logger=logger,
    )


def read(manga_id):
    return standard_request(
        model='manga',
        method='read',
        params={
            'id': str(manga_id),
        },
        logger=logger,
    )


def update(manga_id, name=None, author=None, link=None, active=None):
    return standard_request(
        model='manga',
        method='update',
        params={
            'id': manga_id,
            'name': name,
            'author': author,
            'link': link,
            'active': active,
        },
        logger=logger,
    )


def delete(manga_id):
    return standard_request(
        model='manga',
        method='delete',
        params={
            'id': manga_id,
        },
        logger=logger,
    )


def index():
    """
    [
        {
            "id": int,
            "name": str,
        },
    ]
    """
    return standard_request(
        model='manga',
        method='index',
        params={
        },
        logger=logger,
    )
