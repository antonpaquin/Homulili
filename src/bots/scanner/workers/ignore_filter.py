from queue import Queue
import logging

from dataflow.utils import input_protection
from workers.newfile_filter import NewFile

logger = logging.getLogger(__name__)


@input_protection()
def ignore_filter(input: NewFile, output: Queue):
    logger.debug('Entering ignore_filter')

    # Do weird logic here -- when do we want to ignore a file?
    if False:
        logger.info(
            'For now this is a placeholder -- it should trigger whenever we want to mark ignore a '
            'file off of madokami before it has been downloaded'
        )
        input.ignore = True

    output.put(input)
