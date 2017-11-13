from queue import Queue

import backend
from dataflow.utils import input_protection

from .common import File


@input_protection()
def urls_from_db(input: int, output: Queue):
    print('Enter urls_from_db')
    data = backend.file.index(input)
    for file_json in data:
        output.put(File(
            file_id=file_json['id'],
            manga_id=input,
            url=file_json['url'],
            location=file_json['location'],
            downloaded=file_json['downloaded'],
            ignore=file_json['ignore'],
            parsed=file_json['parsed'],
        ))
