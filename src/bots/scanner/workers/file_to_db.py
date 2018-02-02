import logging

import backend
from dataflow.utils import input_protection
from workers.newfile_filter import NewFile

logger = logging.getLogger(__name__)


@input_protection()
def file_to_db(input: NewFile):
    logger.debug('Entering file_to_db')
    logger.info('Add new file for manga {manga_id}: {url}'.format(
        manga_id=input.manga_id,
        url=input.url,
    ))

    backend.file.create(
        manga_id=input.manga_id,
        file_url=input.url,
        location=input.location,
        state=input.state,
    )
