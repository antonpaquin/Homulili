from flask import request
import logging

from standard_request import standard_request, make_response

import validator
import db
import formatter

logger = logging.getLogger(__name__)


def manga():
    return route_command(command_map={
    })


def chapter():
    return route_command(command_map={
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


def route_command(command_map):
    logger.debug('Entering route_command')
    if 'command' not in request.args:
        logger.warning('Command request did not specify command')
        return make_response({
            'status': 'parameter error',
            'err_message': 'parameter \'command\' must be in all post requests'
        }, code=400)
    command = request.args.get('command')

    if command not in command_map:
        logger.warning('Command request with invalid command: {command}'.format(
            command=command,
        ))
        return make_response({
            'status': 'parameter error',
            'err_message': 'model does not support command \'{command}\''.format(command=command)
        }, code=400)

    logger.info('Handling command request: command={command}'.format(
        command=command,
    ))
    return command_map[command]()
