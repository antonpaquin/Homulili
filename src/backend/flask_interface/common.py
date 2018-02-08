import json
import requests
import logging

from . import config
from . import secret

auth_header = {
    'auth_token': secret.api_admin_key,
}


def standard_request(model: str, method: str, params: dict, logger: logging.Logger):
    method_map = {
        'create': requests.put,
        'read': requests.get,
        'update': requests.patch,
        'delete': requests.delete,
        'index': lambda **x: requests.request(method='VIEW', **x),
        'command': requests.post,
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


