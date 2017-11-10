from flask import request

import backend
from common import render_template


def manga_route_root():
    manga = backend.manga.index()
    return render_template('manga', manga=manga)


def manga_route_create():
    if 'link' in request.args:
        backend.manga.create(
            name=request.args.get('name'),
            author=request.args.get('author'),
            link=request.args.get('link'),
        )
    return render_template('manga_create')
