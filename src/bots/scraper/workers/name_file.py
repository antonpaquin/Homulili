from queue import Queue
import fs.path
import logging

from dataflow.utils import input_protection

import config
from .common import File

logger = logging.getLogger(__name__)

root_dir = fs.path.join('/data', 'raw_files/')


@input_protection()
def name_file(input: File, output: Queue):
    logger.debug('Entering name_file')
    save_dir = fs.path.join(root_dir, str(input.manga_id))
    filename = '{file_id}_-_{remote_name}'.format(
        file_id=input.file_id,
        remote_name=safe_filename(input.url.split('/')[-1])
    )
    logger.info('Decided to name file {filename}'.format(
        filename=filename,
    ))

    input.location = fs.path.join(save_dir, filename)

    output.put(input)


def safe_filename(name: str):
    banned_chars = '!@#$%^&*[]=/\\"\':;?<>~`'
    name = name.replace(' ', '_')
    # noinspection PyTypeChecker
    return name.translate(banned_chars)
