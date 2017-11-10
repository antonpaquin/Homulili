from flask import request

from standard_request import standard_request, make_response

import validator
import db
import formatter


def manga():
    return route_command(command_map={
    })


def chapter():
    return route_command(command_map={
        'reorder': chapter_reorder,
    })


def page():
    return route_command(command_map={
    })


def pagedata():
    return route_command(command_map={
    })


def file():
    return route_command(command_map={
    })


def chapter_reorder():
    if not request.is_json:
        return make_response({
            'status': 'argument error',
            'err_message': 'reorder must be json',
        }, code=400)

    return standard_request(
        params={
            'ids': request.json
        },
        validator=validator.chapter.reorder,
        db_call=db.chapter.reorder,
        formatter=formatter.chapter.reorder,
    )


def route_command(command_map):
    if 'command' not in request.args:
        return make_response({
            'status': 'parameter error',
            'err_message': 'parameter \'command\' must be in all post requests'
        }, code=400)
    command = request.args.get('command')

    if command not in command_map:
        return make_response({
            'status': 'parameter error',
            'err_message': 'model does not support command \'{command}\''.format(command=command)
        }, code=400)

    return command_map[command]()
