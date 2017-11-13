from flask import request
from cryptography.fernet import Fernet
import json
import base64

from standard_request import make_response
import secret


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
    return base64.b64decode(request.headers.get('auth_token') or '')


def err_response(method):
    return make_response({
        'status': 'Authentication Error',
        'err_message': 'You do not have {method} permissions on this object'.format(method=method),
    }, code=401)


# TODO: security with a user database
def authenticate(method):
    token = get_token()

    if not token:
        return False

    if token in cache[method]:
        return True

    plaintext = crypto.decrypt(token).decode()
    try:
        jsn = json.loads(plaintext)
        assert jsn[method]
        cache[method].add(token)
        return True
    except Exception:
        return False
