from queue import Queue
import fs
from fs import zipfs, osfs, path
import zipfile
import logging

from dataflow.utils import input_protection
import backend

from .common import File, Chapter, Page
import config

import workers.unzippers as unzippers

logger = logging.getLogger(__name__)

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
    logger.debug('Entering unzip')

    zip_f = root_filestore.open(input.location, 'rb')
    try:
        zip = zipfs.ReadZipFS(zip_f)
    except zipfile.BadZipFile:
        logger.error('Error -- {file} appears to not be a zipfile, marking for ignore'.format(
            file=input.location))
        backend.file.update(file_id=input.file_id, ignore=True)
        return

    unzip_strategies = [
        unzippers.chapters_in_subdirectories,
        unzippers.zip_containing_zips,
        unzippers.single_chapter,
        unzippers.chapters_in_subdirectories_with_credits
    ]

    success = False

    for strategy in unzip_strategies:
        if strategy.match(zip):
            logger.info('Trying to unzip file {file} with strategy {strategy}'.format(
                file=input.location,
                strategy=strategy.__name__,
            ))
            try:
                success = strategy.process(input, zip, output_chapter, output_page)
            except Exception as e:
                success = False
                logger.error('Unzip failed: {err}'.format(
                    err=str(e),
                ))

        if success:
            logger.info('Success')
            backend.file.update(file_id=input.file_id, state='done')
            break

    zip.close()

    if not success:
        logger.warning('Failed unzipping {file} -- no working strategy'.format(
            file=input.location,
        ))
        backend.file.update(file_id=input.file_id, state='error')
