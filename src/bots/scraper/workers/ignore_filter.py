from queue import Queue

from dataflow.utils import input_protection

from .common import File


@input_protection()
def ignore_filter(input: File, output: Queue):
    if not input.ignore and not input.downloaded:
        output.put(input)
