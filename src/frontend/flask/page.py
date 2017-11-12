from flask import request

import backend
from common import render_template
from security import authenticated
import config


@authenticated
def page_route_index():
    if 'chapter_id' not in request.args:
        return 'none'

    chapter_id = request.args.get('chapter_id')
    pages = backend.page.index(chapter_id)
    return render_template('page_index', pages=pages, chapter_id=chapter_id)


@authenticated
def page_route_display():
    if 'chapter_id' not in request.args:
        return 'none'

    chapter_id = request.args.get('chapter_id')
    chapter = backend.chapter.read(chapter_id)
    pages = backend.page.index(chapter_id)
    return render_template('page_display', pages=pages, chapter=chapter,
                           api_hostname=config.api_hostname, api_public_port=config.api_public_port)


@authenticated
def page_route_rechapter():
    if 'chapter_id' not in request.args:
        return 'none'

    chapter_id = request.args.get('chapter_id')
    pages = backend.page.index(chapter_id)
    chapter = backend.chapter.read(chapter_id)
    return render_template('page_rechapter', pages=pages, chapter=chapter)


@authenticated
def page_route_rechapter_target():
    if not request.is_json:
        return '', 400

    new_chapter = backend.chapter.create(
        manga_id=request.json['manga_id'],
        name=request.json['name'],
        sort_key=request.json['sort_key'],
    )

    for page_id in request.json['page_ids']:
        backend.page.update(
            page_id=page_id,
            chapter_id=new_chapter['id'],
        )

    return '', 200
