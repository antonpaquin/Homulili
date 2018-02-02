import logging

from dataflow.utils import input_protection
import backend

from .common import File

logger = logging.getLogger(__name__)


@input_protection()
def update_db(input: File):
    logger.debug('Entering update_db')
    backend.file.update(
        file_id=input.file_id,
        manga_id=input.manga_id,
        file_url=input.url,
        location=input.location,
        state='downloaded',
    )
