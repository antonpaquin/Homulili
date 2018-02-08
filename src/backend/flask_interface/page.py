import logging

from .common import standard_request

logger = logging.getLogger(__name__)


def create(chapter_id, sort_key, file):
    return standard_request(
        model='page',
        method='create',
        params={
            'chapter_id': chapter_id,
            'sort_key': sort_key,
            'file': file,
        },
        logger=logger,
    )


def read(page_id):
    return standard_request(
        model='page',
        method='read',
        params={
            'id': page_id,
        },
        logger=logger,
    )


def update(page_id, chapter_id=None, sort_key=None, file=None):
    return standard_request(
        model='page',
        method='update',
        params={
            'id': page_id,
            'chapter_id': chapter_id,
            'sort_key': sort_key,
            'file': file
        },
        logger=logger,
    )


def delete(page_id):
    return standard_request(
        model='page',
        method='delete',
        params={
            'id': page_id,
        },
        logger=logger,
    )


def index(chapter_id):
    """
    [
        {
            'id': int,
            'sort_key': int,
        },
    ]
    """
    return standard_request(
        model='page',
        method='index',
        params={
            'chapter_id': chapter_id,
        },
        logger=logger,
    )


def add_mirror(page_id, url):
    return standard_request(
        model='page',
        method='command',
        params={
            'command': 'add_mirror',
            'page_id': page_id,
            'url': url,
        },
        logger=logger,
    )
