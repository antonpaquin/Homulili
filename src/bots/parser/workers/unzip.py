from queue import Queue
import re
import fs
from fs import zipfs, osfs, path

from dataflow.utils import input_protection
import backend

from .common import File, Chapter, Page
import config

import workers.unzippers as unzippers

# noinspection PyUnresolvedReferences
root_filestore = osfs.OSFS(config.pyfs_container)
data_filestore = fs.path.join(config.data_dir, 'raw_files')


@input_protection()
def unzip(input: File, output: Queue):
    """
    First, open the file and try to guess what chapters it contains.
    Emit a chapter object for each chapter.
    Then emit a page for each page in that chapter.

    --

    The chapter/page actors will need to do some state magic to ensure
    pages only get sent after a chapter is sent


    """
    zipfile_f = root_filestore.open(input.location, 'rb')
    zipfile = zipfs.ReadZipFS(zipfile_f)

    unzip_strategies = [
        unzippers.chapters_in_subdirectories,
        unzippers.zip_containing_zips,
        unzippers.single_chapter,
    ]

    success = False

    for strategy in unzip_strategies:
        if strategy.match(zipfile):
            success = strategy.process(input, zipfile, output)

        if success:
            break

    if success:
        backend.file.update(file_id=input.file_id, parsed=True)
    else:
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
