from flask import request
import psycopg2
import logging

from standard_request import make_response
from secret import postgres_password

logger = logging.getLogger(__name__)

conn = psycopg2.connect('dbname=homulili user=homulili host=127.0.0.1 password={postgres_password}'.format(
    postgres_password=postgres_password,
))


def get_token():
    try:
        return request.headers.get('auth_token') or ''
    except Exception as err:
        logger.warning('Could not get auth_token header: {err}'.format(
            err=str(err),
        ))
        return ''


def err_response(method):
    return make_response({
        'status': 'Authentication Error',
        'err_message': 'You do not have {method} permissions on this object'.format(method=method),
    }, code=401)


def authenticate(method):
    token = get_token()

    if not token:
        logger.warning('Denying authentication: no auth_token given')
        return False

    permission_requested = {
        'create': 'p_create',
        'read': 'p_read',
        'update': 'p_update',
        'delete': 'p_delete',
        'index': 'p_index',
        'command': 'p_command',
        'admin': 'p_admin',
    }.get(method, None)

    if not permission_requested:
        logger.error('Denying authentication: requested invalid permission {method}'.format(
            method=method,
        ))
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT %s FROM api_access WHERE api_key = %s',
                (permission_requested, token),
            )
            permission_granted = cur.fetchone()
        assert permission_granted and permission_granted[0]
        return True
    except AssertionError as err:
        logging.warning('Denying authentication: insufficient permissions')
        return False
    except Exception as err:
        logging.warning('Denying authentication: invalid key, {err}'.format(
            err=str(err),
        ))
        return False
