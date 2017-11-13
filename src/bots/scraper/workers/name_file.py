from queue import Queue
import fs.path

from dataflow.utils import input_protection

import config
from .common import File


root_dir = fs.path.join('/data', 'raw_files/')


@input_protection()
def name_file(input: File, output: Queue):
    print('Enter name_file')
    save_dir = fs.path.join(root_dir, str(input.manga_id))
    filename = '{file_id}_-_{remote_name}'.format(
        file_id=input.file_id,
        remote_name=safe_filename(input.url.split('/')[-1])
    )

    input.location = fs.path.join(save_dir, filename)

    output.put(input)


def safe_filename(name: str):
    banned_chars = '!@#$%^&*[]=/\\"\':;?<>~`'
    name = name.replace(' ', '_')
    # noinspection PyTypeChecker
    return name.translate(banned_chars)
