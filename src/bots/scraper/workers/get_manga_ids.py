from queue import Queue

import backend


def get_manga_ids(output: Queue):
    data = backend.manga.index()
    all_manga_ids = [m['id'] for m in data]

    for manga_id in all_manga_ids:
        output.put(manga_id)
