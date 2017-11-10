from dataflow.utils import input_protection
import backend

from .common import Page


@input_protection()
def page_to_db(input: Page):
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

