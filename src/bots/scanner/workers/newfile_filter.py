from datetime import datetime, timedelta
from queue import Queue
from urllib.request import unquote
import logging

import backend
from dataflow.utils import input_protection
from workers.node_url import NodeUrl

logger = logging.getLogger(__name__)


max_fetch_age = timedelta(minutes=30)

downloaded_files = {}  # manga id -> set(file name)
invalidation_timer = {}


class NewFile:
    def __init__(self, manga_id, url, location=None, state='ready'):
        self.manga_id = manga_id
        self.url = url
        self.location = location
        self.state = state


@input_protection()
def newfile_filter(input: NodeUrl, output: Queue):
    logger.debug('Entering newfile_filter')
    if input.manga_id not in downloaded_files or \
            datetime.now() - invalidation_timer[input.manga_id] > max_fetch_age:
        fetch_manga(input.manga_id)

    url = unquote(input.url)

    if url not in downloaded_files[input.manga_id]:
        output.put(NewFile(manga_id=input.manga_id, url=url))

    downloaded_files[input.manga_id].add(url)


def fetch_manga(manga_id):
    logger.info('Checking for already downloaded files for manga_id {manga_id}'.format(
        manga_id=manga_id,
    ))
    if manga_id not in downloaded_files:
        downloaded_files[manga_id] = set()

    data = backend.file.index(manga_id=manga_id)
    for row in data:
        downloaded_files[manga_id].add(unquote(row['url']))

    invalidation_timer[manga_id] = datetime.now()
