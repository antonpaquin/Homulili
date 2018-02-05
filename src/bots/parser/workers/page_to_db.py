from time import sleep
import logging

from dataflow.utils import input_protection
import backend
import cdn

from .common import Page

logger = logging.getLogger(__name__)


max_wait_for_chapter = 15


@input_protection()
def page_to_db(input: Page):
    logger.debug('Entering page_to_db')

    wait_for_chapter = max_wait_for_chapter
    while input.chapter.chapter_id is None:
        wait_for_chapter -= 1
        if wait_for_chapter <= 0:
            logger.error('Waited too long for chapter to get ID')
            raise RuntimeError('Chapter never got ID')
        sleep(1)

    logger.debug('Creating page ({sort_key}) in chapter ({chapter_id})'.format(
        sort_key=input.sort_key,
        chapter_id=input.chapter.chapter_id,
    ))
    page_id = backend.page.create(
        chapter_id=input.chapter.chapter_id,
        sort_key=input.sort_key,
        file=input.file_id,
    )['id']
    cdn.imgdata.upload(input.data)

    input.page_id = page_id
