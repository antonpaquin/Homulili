from queue import Queue

from dataflow.utils import input_protection
import backend

from .common import File


@input_protection()
def files_from_db(input: int, output: Queue):
    data = backend.file.index(input)

    for row in data:
        if not row['parsed'] and not row['ignore'] and row['downloaded']:
            output.put(File(
                manga_id=input,
                location=row['location'],
                file_id=row['id'],
            ))
