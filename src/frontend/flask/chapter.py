from flask import request

import backend
from common import render_template
from security import authenticated


@authenticated
def chapter_route_index():
    if 'manga_id' not in request.args:
        return '', 400

    manga_id = request.args.get('manga_id')
    manga = backend.manga.read(manga_id)
    chapters = backend.chapter.index(manga_id)
    return render_template('chapter_index', manga=manga, chapters=chapters)


@authenticated
def chapter_route_rename_target():
    if 'chapter_id' not in request.args or 'name' not in request.args:
        return '', 400

    chapter_id = request.args.get('chapter_id')
    name = request.args.get('name')
    backend.chapter.update(chapter_id=chapter_id, name=name)
    return '', 200


@authenticated
def chapter_route_delete_target():
    if 'chapter_id' not in request.args:
        return '', 400

    chapter_id = request.args.get('chapter_id')
    backend.chapter.delete(chapter_id)
    return '', 200


@authenticated
def chapter_route_resort_target():
    if 'chapter_id' not in request.args:
        return '', 400

    chapter_id = request.args.get('chapter_id')
    sort_key = request.args.get('sort_key')
    backend.chapter.update(chapter_id, sort_key=sort_key)
    return '', 200
