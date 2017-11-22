import fs
from fs import zipfs, tempfs, path
from queue import Queue
import logging

from workers.common import File, Chapter, Page
from workers.unzippers.common import guess_chapter

logger = logging.getLogger(__name__)


def match(zipfile: zipfs.ReadZipFS):
    root_dir = zipfile.listdir('/')
    for elem in root_dir:
        if not zipfile.isfile(elem):
            return False
        if not fs.path.split(elem)[-1].split('.')[-1] == 'zip':
            return False
    return True


def process(input: File, zipfile: zipfs.ReadZipFS, output_chapter: Queue, output_page: Queue):
    logger.debug('Entering zip_containing_zips processing stage')
    unzip_tmpfs = fs.tempfs.TempFS()
    subzips = zipfile.listdir('/')
    logger.info('Unzipping found ({num_chapters}) chapters'.format(
        num_chapters=len(subzips),
    ))
    for subzip in subzips:
        chapter_number = guess_chapter(subzip)
        chapter = Chapter(
            manga_id=input.manga_id,
            name=str(chapter_number),
            sort_key=chapter_number,
        )

        output_chapter.put(chapter)

        logger.info('Starting to extract subzip to tmpfs')

        with zipfile.open(subzip, 'rb') as opened_zip:
            with unzip_tmpfs.open(subzip, 'wb') as tmpfs_f:
                tmpfs_f.write(opened_zip.read())

        logger.info('Tmpfs extraction successful')
        logger.info('Starting to read inner zip')

        tmpfs_f = unzip_tmpfs.open(subzip, 'rb')
        subdir = zipfs.ReadZipFS(tmpfs_f)

        pages = subdir.listdir('/')

        # Hack: if the zip contains a single directory, cd into that one instead
        # Fucking zip maintainers
        if len(pages) == 1 and subdir.isdir(pages[0]):
            logger.info('Subzip was of a directory containing files -- changing dir')
            pages = [fs.path.join(pages[0], x) for x in subdir.listdir(pages[0])]

        pages.sort()
        logger.info('Chapter has ({num_pages}) pages'.format(
            num_pages=len(pages),
        ))
        for idx, pagename in enumerate(pages):
            with subdir.open(fs.path.join('/', pagename), 'rb') as page_f:
                # noinspection PyUnresolvedReferences
                data = page_f.read()

            page = Page(
                chapter=chapter,
                sort_key=idx,
                file_id=input.file_id,
                data=data,
            )

            chapter.num_pages += 1

            output_page.put(page)

        tmpfs_f.close()
        subdir.close()

    unzip_tmpfs.close()
    return True
