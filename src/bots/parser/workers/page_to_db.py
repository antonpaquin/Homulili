from dataflow.utils import input_protection
import backend
from time import sleep

from .common import Page

max_wait_for_chapter = 15


@input_protection()
def page_to_db(input: Page):

    wait_for_chapter = max_wait_for_chapter
    while input.chapter.chapter_id is None:
        wait_for_chapter -= 1
        if wait_for_chapter <= 0:
            raise RuntimeError('Chapter never got ID')
        sleep(1)

    page_id = backend.page.create(
        chapter_id=input.chapter.chapter_id,
        sort_key=input.sort_key,
        file=input.file_id,
    )['id']

    input.page_id = page_id

    backend.pagedata.create(
        page_id=page_id,
        data=input.data,
    )

