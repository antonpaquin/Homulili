from queue import Queue

from dataflow.utils import input_protection
from workers.newfile_filter import NewFile


@input_protection()
def ignore_filter(input: NewFile, output: Queue):

    # Do weird logic here -- when do we want to ignore a file?
    if False:
        input.ignore = True

    output.put(input)
