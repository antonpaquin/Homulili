from flask import request

import backend
from common import render_template
from security import authenticated


@authenticated
def manga_route_index():
    manga = backend.manga.index()
    return render_template('manga_index', manga=manga)


@authenticated
def manga_route_create_target():
    if 'link' not in request.args:
        return '', 400

    name = request.args.get('name')
    author = request.args.get('author')
    link = request.args.get('link')

    response = backend.manga.create(name=name, author=author, link=link)

    return str(response['id']), 200


@authenticated
def manga_route_delete_target():
    if 'manga_id' not in request.args:
        return '', 400

    manga_id = request.args.get('manga_id')
    backend.manga.delete(manga_id=manga_id)
    return '', 200


@authenticated
def manga_route_rename_target():
    if 'manga_id' not in request.args or 'name' not in request.args:
        return '', 400

    manga_id = request.args.get('manga_id')
    name = request.args.get('name')
    backend.manga.update(manga_id=manga_id, name=name)
    return '', 200
