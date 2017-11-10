import fs
from fs import zipfs, path
from queue import Queue

from workers.common import File, Chapter, Page
from workers.unzippers.common import guess_chapter


def match(zipfile: zipfs.ReadZipFS):
    root_dir = zipfile.listdir('/')
    for page in root_dir:
        if not zipfile.isfile(page):
            return False
    return True


def process(input: File, zipfile: zipfs.ReadZipFS, output: Queue):
    filename = fs.path.split(input.location)[-1]
    chapter_number = guess_chapter(filename)
    chapter = Chapter(
        manga_id=input.manga_id,
        name=str(chapter_number),
        sort_key=chapter_number,
    )
    pages = zipfile.listdir('/')
    pages.sort()
    for idx, page in enumerate(pages):
        with zipfile.open(fs.path.join('/', page), 'rb') as page_f:
            # noinspection PyUnresolvedReferences
            data = page_f.read()

        chapter.add_page(Page(
            chapter=chapter,
            sort_key=idx,
            file_id=input.file_id,
            data=data,
        ))

    output.put(chapter)

    return True
