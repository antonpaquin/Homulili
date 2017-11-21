from queue import Queue
import logging

from dataflow.utils import input_protection
import backend

from .common import Chapter

logger = logging.getLogger(__name__)


@input_protection()
def chapter_to_db(input: Chapter):
    logger.debug('Entering chapter_to_db')

    chapter_id = backend.chapter.create(
        manga_id=input.manga_id,
        name=input.name,
        sort_key=input.sort_key,
    )['id']

    logger.info(
        'Added new chapter ({sort_key}) with id ({chapter_id}) to manga ({manga_id}) with ({num_pages}) pages'.format(
            sort_key=input.sort_key,
            chapter_id=chapter_id,
            manga_id=input.manga_id,
            num_pages=len(input.pages),
        )
    )

    input.chapter_id = chapter_id
