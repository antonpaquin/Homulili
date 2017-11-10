from queue import Queue

from dataflow.utils import input_protection
import backend

from .common import Chapter


@input_protection()
def chapter_to_db(input: Chapter, output: Queue):
    chapter_id = backend.chapter.create(
        manga_id=input.manga_id,
        name=input.name,
        sort_key=input.sort_key,
    )['id']

    print('Adding chapter ({chapter_id}) to manga ({manga_id}) with ({num_pages}) pages'.format(
        chapter_id=chapter_id,
        manga_id=input.manga_id,
        num_pages=len(input.pages),
    ))

    input.chapter_id = chapter_id

    for page in input.pages:
        output.put(page)
