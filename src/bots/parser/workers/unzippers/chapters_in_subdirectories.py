import fs
from fs import zipfs, path
from queue import Queue
import logging

from workers.common import File, Chapter, Page
from workers.unzippers.common import guess_chapter

logger = logging.getLogger(__name__)


def match(zipfile: zipfs.ReadZipFS):
    """ If the file matches: all directories in the root, each containing all files, it's probably
    /chapter/page"""
    root_dir = zipfile.listdir('/')
    for subdir in root_dir:
        if not zipfile.isdir(subdir):
            return False
        subpages = zipfile.listdir(subdir)
        for page in subpages:
            if not zipfile.isfile(fs.path.join('/', subdir, page)):
                return False
    return True


def process(input: File, zipfile: zipfs.ReadZipFS, output_chapter: Queue, output_page: Queue):
    logger.debug('Entering chapters_in_subdirectories processing stage')
    subdirs = zipfile.listdir('/')
    logger.info('Unzipping found ({num_chapters}) chapters'.format(
        num_chapters=len(subdirs),
    ))
    for subdir in subdirs:
        chapter_number = guess_chapter(subdir)
        chapter = Chapter(
            manga_id=input.manga_id,
            name=str(chapter_number),
            sort_key=chapter_number,
        )

        output_chapter.put(chapter)

        pages = zipfile.listdir(subdir)
        pages.sort()
        logger.info('Chapter has ({num_pages}) pages'.format(
            num_pages=len(pages),
        ))
        for idx, pagename in enumerate(pages):
            with zipfile.open(fs.path.join('/', subdir, pagename), 'rb') as page_f:
                # noinspection PyUnresolvedReferences
                data = page_f.read()

            page = Page(
                chapter=chapter,
                sort_key=idx,
                file_id=input.file_id,
                data=data,
            )

            output_page.put(page)

    return True
