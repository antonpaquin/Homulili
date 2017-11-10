from queue import Queue

import flask_interface
from dataflow.utils import input_protection


class HeadUrl:
    def __init__(self, manga_id, url):
        self.manga_id = manga_id
        self.url = url


@input_protection(num_inputs=0)
def head_url(output: Queue):
    data = flask_interface.manga.index()
    all_manga_ids = [row['id'] for row in data]

    for manga_id in all_manga_ids:
        data = flask_interface.manga.read(manga_id=manga_id)
        output.put(HeadUrl(
            manga_id=manga_id,
            url=data['madokami_url']
        ))
