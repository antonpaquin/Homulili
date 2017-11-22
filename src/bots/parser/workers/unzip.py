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

    # Precheck: make sure that the file is still unparsed as we expect
    file = backend.file.read(file_id=input.file_id)
    if file['parsed']:
        logger.debug('Abandoning file -- it appears to have already been parsed')
        return

    # Precheck: make sure file is zip
    if not zipfile.is_zipfile(input.location):
        logger.error('Error -- {file} appears to not be a zipfile, marking for ignore'.format(
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
            logger.info('Trying to unzip file {file} with strategy {strategy}'.format(
                file=input.location,
                strategy=strategy.__name__,
            ))
            success = strategy.process(input, zip, output_chapter, output_page)

        if success:
            logger.info('Success')
            break

    zip.close()

    if not success:
        backend.file.update(file_id=input.file_id, parsed=False)
        logger.warning('Failed unzipping {file} -- no matching strategy'.format(
            file=input.location,
        ))
