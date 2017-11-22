from queue import Queue
import logging

import backend
from dataflow.utils import input_protection

logger = logging.getLogger(__name__)


class HeadUrl:
    def __init__(self, manga_id, url):
        self.manga_id = manga_id
        self.url = url


@input_protection(num_inputs=0)
def head_url(output: Queue):
    logger.debug('Entering head_url')
    data = backend.manga.index()
    all_manga_ids = [row['id'] for row in data]

    logger.info('Sending {num_ids} to pipeline'.format(
        num_ids=len(all_manga_ids),
    ))

    for manga_id in all_manga_ids:
        data = backend.manga.read(manga_id=manga_id)
        output.put(HeadUrl(
            manga_id=manga_id,
            url=data['madokami_url']
        ))
