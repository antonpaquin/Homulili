from flask import request
import logging

import backend
from common import render_template
from security import authenticated
import config

logger = logging.getLogger(__name__)


@authenticated
def page_route_display():
    logger.info('Responding to page::index')
    if 'chapter_id' not in request.args:
        logger.warning('Insufficient arguments')
        return 'none'

    chapter_id = request.args.get('chapter_id')
    chapter = backend.chapter.read(chapter_id)
    pages = backend.page.index(chapter_id)
    return render_template('page_display', pages=pages, chapter=chapter,
                           api_hostname=config.api_hostname, api_public_port=config.api_public_port)


@authenticated
def page_route_rechapter_target():
    logger.info('Responding to page::rechapter')
    if not request.is_json:
        logger.warning('Rechapter arguments is not JSON')
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
