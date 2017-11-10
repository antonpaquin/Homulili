from queue import Queue

import flask_interface


def get_manga_ids(output: Queue):
    print('Enter get_manga_ids')
    data = flask_interface.manga.index()
    all_manga_ids = [m['id'] for m in data]

    for manga_id in all_manga_ids:
        output.put(manga_id)
