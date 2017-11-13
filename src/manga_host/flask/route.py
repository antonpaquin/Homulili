from __future__ import absolute_import

import flask
from flask import Flask, request
import json

from standard_request import standard_request
import db
import validator
import formatter
import security

import config
import route_commands


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
        response = flask.Response()
        response.headers.set('Allow', ','.join([
            'PUT', 'GET', 'PATCH', 'DELETE', 'VIEW', 'OPTIONS', 'POST',
        ]))
        return response

    if request.method not in method_map:
        return 'Invalid method'

    method = method_map[request.method]

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
                'downloaded': 'downloaded',
                'ignore': 'ignore',
                'parsed': 'parsed',
            },
            'read': {
                'file_id': 'id',
            },
            'update': {
                'file_id': 'id',
                'manga_id': 'manga_id',
                'url': 'url',
                'location': 'location',
                'downloaded': 'downloaded',
                'ignore': 'ignore',
                'parsed': 'parsed',
            },
            'delete': {
                'file_id': 'id',
            },
            'index': {
                'manga_id': 'manga_id',
            },
        },
        route_validator=validator.file,
        route_db=db.file,
        route_formatter=formatter.file,
        commands=route_commands.file,
    )


# noinspection PyTypeChecker
@app.route('/pagedata', methods=['GET', 'PUT', 'DELETE', 'OPTIONS', 'POST'])
def pagedata():
    auth_token = request.headers.get('auth_token')

    if request.method == 'PUT':
        if not security.authenticate('create'):
            return security.err_response('create')
        return standard_request(
            params={
                'page_id': request.args.get('page_id'),
                'data': request.data,
            },
            validator=validator.pagedata.create,
            db_call=db.pagedata.create,
            formatter=formatter.pagedata.create,
        )

    elif request.method == 'GET':
        if not security.authenticate('read'):
            return security.err_response('read')
        response = flask.Response()
        try:
            args = {'page_id': int(request.args.get('page_id'))}
            data = db.pagedata.read(**args)
            response.set_data(formatter.pagedata.read(data, args))
            response.headers.set('Content-Type', 'image/png')
            response.status_code = 200
            return response
        except RuntimeError as e:
            response.set_data(json.dumps({'status': 'database error', 'err_message': str(e)}))
            response.status_code = 500
            return response

    elif request.method == 'DELETE':
        if not security.authenticate('delete'):
            return security.err_response('delete')
        return standard_request(
            params={
                'page_id': request.args.get('page_id'),
            },
            validator=validator.pagedata.delete,
            db_call=db.pagedata.delete,
            formatter=formatter.pagedata.delete,
        )

    elif request.method == 'OPTIONS':
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.api_internal_port)
