from queue import Queue
import logging

import backend
from dataflow.utils import input_protection

from .common import File

logger = logging.getLogger(__name__)


@input_protection()
def urls_from_db(input: int, output: Queue):
    logger.debug('Entering urls_from_db')
    data = backend.file.index(manga_id=input, state='ready')
    for file_json in data:
        backend.file.update(file_id=file_json['id'], state='downloading')
        output.put(File(
            file_id=file_json['id'],
            manga_id=input,
            url=file_json['url'],
            location=file_json['location'],
            state=file_json['state'],
        ))
