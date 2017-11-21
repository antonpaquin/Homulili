from queue import Queue
import re
import fs
from fs import zipfs, osfs, path
import zipfile

from dataflow.utils import input_protection
import backend

from .common import File, Chapter, Page
import config

import workers.unzippers as unzippers

# noinspection PyUnresolvedReferences
root_filestore = osfs.OSFS(config.storage_dir)
data_filestore = fs.path.join('/data', 'raw_files')


@input_protection()
def unzip(input: File, output_chapter: Queue, output_page: Queue):
    """
    First, open the file and try to guess what chapters it contains.
    Emit a chapter object for each chapter.
    Then emit a page for each page in that chapter.

    --

    """
    # Precheck: make sure that the file is still unparsed as we expect
    file = backend.file.read(file_id=input.file_id)
    if file['parsed']:
        return

    # Precheck: make sure file is zip
    if not zipfile.is_zipfile(input.location):
        print('Error -- {file} appears to not be a zipfile'.format(
            file=input.location))
        backend.file.update(file_id=input.file_id, ignore=True)
        return

    zip_f = root_filestore.open(input.location, 'rb')
    zip = zipfs.ReadZipFS(zip_f)

    unzip_strategies = [
        unzippers.chapters_in_subdirectories,
        unzippers.zip_containing_zips,
        unzippers.single_chapter,
        unzippers.chapters_in_subdirectories_with_credits
    ]

    success = False

    for strategy in unzip_strategies:
        if strategy.match(zip):
            backend.file.update(file_id=input.file_id, parsed=True)
            success = strategy.process(input, zip, output_chapter, output_page)

        if success:
            break

    zip.close()

    if not success:
        backend.file.update(file_id=input.file_id, parsed=False)
        print('Failed unzipping {file}'.format(file=input.location))


def guess_chapter(filename):
    try:
        cname = re.search('[cC][0-9]+', filename).group()
        return int(cname[1:])
    except Exception:
        pass

    print(filename)
    raise Exception


def get_number(name):
    try:
        return int(re.search('[0-9]+', name).group())
    except Exception:
        pass

    print(name)
    raise Exception
