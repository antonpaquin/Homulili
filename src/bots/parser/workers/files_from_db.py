from queue import Queue
import logging

from dataflow.utils import input_protection
import backend

from .common import File

logger = logging.getLogger(__name__)


@input_protection()
def files_from_db(input: int, output: Queue):
    logger.debug('Entering files_from_db')

    data = backend.file.index(input)

    logger.debug('Scanned {length} files'.format(
        length=len(data),
    ))

    for row in data:
        if not row['parsed'] and not row['ignore'] and row['downloaded']:
            output.put(File(
                manga_id=input,
                location=row['location'],
                file_id=row['id'],
            ))
