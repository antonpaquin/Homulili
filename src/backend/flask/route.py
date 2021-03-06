from __future__ import absolute_import

import flask
from flask import Flask, request
import json
import logging

from standard_request import standard_request
import db
import validator
import formatter
import security

import config
import route_commands


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/backend.log',
    filemode='w',
)
logger = logging.getLogger('route')


logger.info('Starting backend')

app = Flask(__name__)


def standard_route(param_map, route_validator, route_db, route_formatter, commands=None):
    method_map = {
        'PUT': 'create',
        'GET': 'read',
        'PATCH': 'update',
        'DELETE': 'delete',
        'VIEW': 'index',
        'POST': 'command',
    }

    if request.method == 'OPTIONS':
        logger.info('Handling OPTIONS request')
        response = flask.Response()
        response.headers.set('Allow', ','.join([
            'PUT', 'GET', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST',
        ]))
        return response

    if request.method not in method_map:
        logger.warning('Received request with invalid route: {model}::{method}'.format(
            model=request.path,
            method=request.method,
        ))
        return 'Invalid method', 400

    method = method_map[request.method]

    logger.info('Handling request: {model}::{method}'.format(
        model=request.path,
        method=method,
    ))

    if not security.authenticate(method):
        return security.err_response(method)

    if commands and method == 'command':
        return commands()

    params = {}
    for key, value in param_map[method].items():
        if value in request.args:
            params[key] = request.args.get(value)

    return standard_request(
        params=params,
        validator=route_validator.__dict__[method],
        db_call=route_db.__dict__[method],
        formatter=route_formatter.__dict__[method],
    )


# noinspection PyTypeChecker
@app.route('/manga', methods=['GET', 'PUT', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST'])
def manga():
    return standard_route(
        param_map={
            'create': {
                'manga_name': 'name',
                'author': 'author',
                'madokami_link': 'link',
            },
            'read': {
                'manga_id': 'id',
            },
            'update': {
                'manga_id': 'id',
                'manga_name': 'name',
                'author': 'author',
                'madokami_link': 'link',
                'active': 'active',
            },
            'delete': {
                'manga_id': 'id',
            },
            'index': {
            }
        },
        route_validator=validator.manga,
        route_db=db.manga,
        route_formatter=formatter.manga,
        commands=route_commands.manga,
    )


# noinspection PyTypeChecker
@app.route('/chapter', methods=['GET', 'PUT', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST'])
def chapter():
    return standard_route(
        param_map={
            'create': {
                'manga_id': 'manga_id',
                'chapter_name': 'name',
                'sort_key': 'sort_key',
            },
            'read': {
                'chapter_id': 'id',
            },
            'update': {
                'chapter_id': 'id',
                'chapter_name': 'name',
                'manga_id': 'manga_id',
                'sort_key': 'sort_key',
            },
            'delete': {
                'chapter_id': 'id',
            },
            'index': {
                'manga_id': 'manga_id',
            },
        },
        route_validator=validator.chapter,
        route_db=db.chapter,
        route_formatter=formatter.chapter,
        commands=route_commands.chapter,
    )


# noinspection PyTypeChecker
@app.route('/page', methods=['GET', 'PUT', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST'])
def page():
    return standard_route(
        param_map={
            'create': {
                'chapter_id': 'chapter_id',
                'sort_key': 'sort_key',
                'file_id': 'file',
            },
            'read': {
                'page_id': 'id',
            },
            'update': {
                'page_id': 'id',
                'chapter_id': 'chapter_id',
                'sort_key': 'sort_key',
                'file_name': 'file',
            },
            'destroy': {
                'page_id': 'id',
            },
            'index': {
                'chapter_id': 'chapter_id',
            },
            'command': True,
        },
        route_validator=validator.page,
        route_db=db.page,
        route_formatter=formatter.page,
        commands=route_commands.page,
    )


# noinspection PyTypeChecker
@app.route('/file', methods=['GET', 'PUT', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST'])
def file():
    return standard_route(
        param_map={
            'create': {
                'manga_id': 'manga_id',
                'url': 'url',
                'location': 'location',
                'state': 'state',
            },
            'read': {
                'file_id': 'id',
            },
            'update': {
                'file_id': 'id',
                'manga_id': 'manga_id',
                'url': 'url',
                'location': 'location',
                'state': 'state',
            },
            'delete': {
                'file_id': 'id',
            },
            'index': {
                'manga_id': 'manga_id',
                'state': 'state',
            },
        },
        route_validator=validator.file,
        route_db=db.file,
        route_formatter=formatter.file,
        commands=route_commands.file,
    )


# noinspection PyTypeChecker
@app.route('/admin', methods=['GET', 'PUT', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST'])
def admin():
    if not security.authenticate('admin'):
        return security.err_response('admin')

    return standard_route(
        param_map={
            'create': {
                'create': 'create',
                'read': 'read',
                'update': 'update',
                'delete': 'delete',
                'index': 'index',
                'command': 'command',
                'admin': 'admin',
            },
            'read': {
                'api_key': 'api_key',
            },
            'update': {
                'api_key': 'api_key',
                'create': 'create',
                'read': 'read',
                'update': 'update',
                'delete': 'delete',
                'index': 'index',
                'command': 'command',
                'admin': 'admin',
            },
            'delete': {
                'api_key': 'api_key',
            },
        },
        route_validator=validator.admin,
        route_db=db.admin,
        route_formatter=formatter.admin,
        commands=route_commands.admin,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config.api_internal_port))
