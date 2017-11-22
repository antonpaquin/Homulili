import logging

from .common import standard_request

logger = logging.getLogger(__name__)


def create(manga_id, name, sort_key):
    return standard_request(
        model='chapter',
        method='create',
        params={
            'manga_id': manga_id,
            'name': name,
            'sort_key': sort_key,
        },
        logger=logger,
    )


def read(chapter_id):
    return standard_request(
        model='chapter',
        method='read',
        params={
            'id': chapter_id,
        },
        logger=logger,
    )


def update(chapter_id, name=None, manga_id=None, sort_key=None):
    return standard_request(
        model='chapter',
        method='update',
        params={
            'id': chapter_id,
            'name': name,
            'manga_id': manga_id,
            'sort_key': sort_key,
        },
        logger=logger,
    )


def delete(chapter_id):
    return standard_request(
        model='chapter',
        method='delete',
        params={
            'id': chapter_id,
        },
        logger=logger,
    )


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
    return standard_request(
        model='chapter',
        method='index',
        params={
            'manga_id': manga_id,
        },
        logger=logger,
    )
