from cryptography.fernet import Fernet
import json
import base64
import requests
import logging

from . import config
from . import secret

crypto = Fernet(bytes.fromhex(secret.auth_key))

permissions = json.dumps({
    'create': True,
    'read': True,
    'update': True,
    'delete': True,
    'index': True,
    'command': True,
}).encode('utf-8')
auth_token = base64.b64encode(crypto.encrypt(permissions)).decode()

auth_header = {
    'auth_token': auth_token,
}


def standard_request(model: str, method: str, params: dict, logger: logging.Logger):
    method_map = {
        'create': requests.put,
        'read': requests.get,
        'update': requests.patch,
        'delete': requests.delete,
        'index': lambda **x: requests.request(method='VIEW', **x)
    }

    pparams = {key: value for key, value in params.items() if value is not None}

    logger.info('{model}::{method} with params {params}'.format(
        method=method,
        model=model,
        params=str(pparams),
    ))

    url = 'http://{hostname}:{port}/{model}'.format(
        hostname=config.api_hostname,
        port=config.api_public_port,
        model=model,
    )

    requests_call = method_map[method]

    response = requests_call(
        url=url,
        headers=auth_header,
        params=pparams,
    )

    try:
        jsn = json.loads(response.text)
    except Exception:
        logger.error('{method} failed -- response was not json -- {resp}'.format(
            method=method,
            resp=response.text,
        ))
        raise RuntimeError(response.text)

    if jsn['status'] == 'success':
        return jsn['data']
    else:
        logger.error('{method} failed -- err: {err_message}'.format(
            method=method,
            err_message=jsn['err_message'],
        ))
        raise RuntimeError(jsn)


