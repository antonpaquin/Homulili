from queue import Queue
import logging

import backend

logger = logging.getLogger(__name__)


def get_manga_ids(output: Queue):
    logger.debug('Entering get_manga_ids')

    data = backend.manga.index()
    all_manga_ids = [m['id'] for m in data]

    logger.debug('Parsing: {len} ids'.format(
        len=len(all_manga_ids)
    ))

    for manga_id in all_manga_ids:
        output.put(manga_id)
