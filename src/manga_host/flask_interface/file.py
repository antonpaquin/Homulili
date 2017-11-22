import logging

from .common import standard_request

logger = logging.getLogger(__name__)


def create(manga_id, file_url, location=None, downloaded=False, ignore=False, parsed=False):
    return standard_request(
        model='file',
        method='create',
        params={
            'manga_id': manga_id,
            'url': file_url,
            'location': location,
            'downloaded': downloaded,
            'ignore': ignore,
            'parsed': parsed,
        },
        logger=logger,
    )


def read(file_id):
    """
    {
        "url": "https://manga.madokami.al/Manga/N/NE/NEKO/Neko Musume Michikusa Nikki/Neko Musume Michikusa Nikki - v10 c58 [batoto - placeholder scanlations].zip",
        "location": "/data/raw_files/2/40_-_Neko_Musume_Michikusa_Nikki_-_v10_c58_[batoto_-_placeholder_scanlations].zip",
        "time_created": "2017-11-14T19:26:14",
        "ignore": false,
        "manga_id": 2,
        "downloaded": true,
        "id": 40,
        "parsed": true,
        "time_updated": "2017-11-16T22:00:59"
    }
    """
    return standard_request(
        model='file',
        method='read',
        params={
            'id': file_id,
        },
        logger=logger,
    )


def update(file_id, manga_id=None, file_url=None, location=None, downloaded=None, ignore=None, parsed=None):
    return standard_request(
        model='file',
        method='update',
        params={
            'id': file_id,
            'manga_id': manga_id,
            'url': file_url,
            'location': location,
            'downloaded': downloaded,
            'ignore': ignore,
            'parsed': parsed,
        },
        logger=logger,
    )


def delete(file_id):
    return standard_request(
        model='file',
        method='delete',
        params={
            'id': file_id,
        },
        logger=logger,
    )


def index(manga_id):
    return standard_request(
        model='file',
        method='index',
        params={
            'manga_id': manga_id,
        },
        logger=logger,
    )
