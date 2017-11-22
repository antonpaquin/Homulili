from queue import Queue
import logging

from dataflow.utils import input_protection

from .common import File

logger = logging.getLogger(__name__)


@input_protection()
def ignore_filter(input: File, output: Queue):
    logger.debug('Entering ignore_filter')
    if not input.ignore and not input.downloaded:
        output.put(input)
