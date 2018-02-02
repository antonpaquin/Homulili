from queue import Queue
import logging

from dataflow.utils import input_protection
import backend

from .common import File

logger = logging.getLogger(__name__)


@input_protection()
def files_from_db(input: int, output: Queue):
    logger.debug('Entering files_from_db')

    data = backend.file.index(manga_id=input, state='downloaded')

    logger.debug('Scanned {length} files'.format(
        length=len(data),
    ))

    for row in data:
        backend.file.update(file_id=row['id'], state='parsing')
        output.put(File(
            manga_id=input,
            location=row['location'],
            file_id=row['id'],
        ))
