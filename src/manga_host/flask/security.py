from flask import request
from cryptography.fernet import Fernet
import json
import base64
import logging

from standard_request import make_response
import secret

logger = logging.getLogger(__name__)

crypto = Fernet(bytes.fromhex(secret.auth_key))

cache = {
    'create': set(),
    'read': set(),
    'update': set(),
    'delete': set(),
    'index': set(),
    'command': set(),
}


def get_token():
    try:
        return base64.b64decode(request.headers.get('auth_token') or '')
    except Exception as err:
        logger.warning('Could not b64decode auth_token header: {err}'.format(
            err=str(err),
        ))
        return ''


def err_response(method):
    return make_response({
        'status': 'Authentication Error',
        'err_message': 'You do not have {method} permissions on this object'.format(method=method),
    }, code=401)


# TODO: security with a user database
def authenticate(method):
    token = get_token()

    if not token:
        logger.warning('Denying authentication: no auth_token given')
        return False

    if token in cache[method]:
        logger.info('Accepting cached auth key')
        return True

    try:
        plaintext = crypto.decrypt(token).decode()
        jsn = json.loads(plaintext)
        assert jsn[method]
        cache[method].add(token)
        return True
    except AssertionError as err:
        logging.warning('Denying authentication: insufficient permissions')
        return False
    except Exception as err:
        logging.warning('Denying authentication: invalid key, {err}'.format(
            err=str(err),
        ))
        return False
