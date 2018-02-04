from flask import request
import logging
from datetime import datetime

import backend
from common import render_template
from security import authenticated

logger = logging.getLogger(__name__)


@authenticated
def manga_route_index(api_key):
    logger.info('Responding to manga::index')
    manga = backend.manga.index()
    return render_template('manga_index', manga=manga)


@authenticated
def manga_route_rss(api_key):
    logger.info('Responding to manga::rss')
    if 'manga_id' not in request.args:
        logger.warning('manga_id not in parameters, cannot generate rss')
        return '', 400

    manga_id = request.args.get('manga_id')
    manga = backend.manga.read(manga_id)
    chapters = backend.chapter.index(manga_id)
    meta = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    return (
        render_template('manga_rss', manga=manga, chapters=chapters, meta=meta),
        200,
        {'Content-Type': 'application/xml'}
    )


@authenticated
def manga_route_create_target(api_key):
    logger.info('Responding to manga::create')
    if 'link' not in request.args:
        logger.warning('link not in parameters, cannot create')
        return '', 400

    name = request.args.get('name')
    author = request.args.get('author')
    link = request.args.get('link')

    response = backend.manga.create(name=name, author=author, link=link)

    return str(response['id']), 200


@authenticated
def manga_route_delete_target(api_key):
    logger.info('Responding to manga::delete')
    if 'manga_id' not in request.args:
        logger.warning('manga_id not in parameters, cannot delete')
        return '', 400

    manga_id = request.args.get('manga_id')
    backend.manga.delete(manga_id=manga_id)
    return '', 200


@authenticated
def manga_route_rename_target(api_key):
    logger.info('Responding to manga::rename')
    if 'manga_id' not in request.args or 'name' not in request.args:
        logger.warning('Insufficient parameters')
        return '', 400

    manga_id = request.args.get('manga_id')
    name = request.args.get('name')
    backend.manga.update(manga_id=manga_id, name=name)
    return '', 200
