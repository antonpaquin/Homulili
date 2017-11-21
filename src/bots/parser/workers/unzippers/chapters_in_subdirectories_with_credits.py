import fs
from fs import zipfs, path
from queue import Queue

from workers.common import File, Chapter, Page
from workers.unzippers.common import guess_chapter


max_credit_threshold = 1
min_dir_threshold = 1


def match(zipfile: zipfs.ReadZipFS):
    """ Same as chapters in subdirs, with the allowance of a threshold number of credits pages
    in the top level dir """

    count_pages = 0
    count_dirs = 0
    root_dir = zipfile.listdir('/')
    for subdir in root_dir:
        if not zipfile.isdir(subdir):
            count_pages += 1
            continue
        else:
            count_dirs += 1

        subpages = zipfile.listdir(subdir)
        for page in subpages:
            if not zipfile.isfile(fs.path.join('/', subdir, page)):
                return False

    if count_pages > max_credit_threshold or count_dirs < min_dir_threshold:
        return False

    return True


def process(input: File, zipfile: zipfs.ReadZipFS, output_chapter: Queue, output_page: Queue):
    for subdir in zipfile.listdir('/'):
        if zipfile.isfile(subdir):
            continue

        chapter_number = guess_chapter(subdir)
        chapter = Chapter(
            manga_id=input.manga_id,
            name=str(chapter_number),
            sort_key=chapter_number,
        )

        output_chapter.put(chapter)

        pages = zipfile.listdir(subdir)
        pages.sort()
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
