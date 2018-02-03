import logging

from .common import standard_request

logger = logging.getLogger(__name__)


def create(p_create=False, p_read=False, p_update=False, p_delete=False, p_index=False, p_command=False, p_admin=False):
    return standard_request(
        model='admin',
        method='create',
        params={
            'create': p_create,
            'read': p_read,
            'update': p_update,
            'delete': p_delete,
            'index': p_index,
            'command': p_command,
            'admin': p_admin,
        },
        logger=logger,
    )


def read(api_key):
    return standard_request(
        model='admin',
        method='read',
        params={
            'api_key': api_key,
        },
        logger=logger,
    )


def update(api_key, p_create=None, p_read=None, p_update=None, p_delete=None,
           p_index=None, p_command=None, p_admin=None):
    return standard_request(
        model='admin',
        method='update',
        params={
            'api_key': api_key,
            'create': p_create,
            'read': p_read,
            'update': p_update,
            'delete': p_delete,
            'index': p_index,
            'command': p_command,
            'admin': p_admin,
        },
        logger=logger,
    )


def delete(api_key):
    return standard_request(
        model='admin',
        method='delete',
        params={
            'api_key': api_key,
        },
        logger=logger,
    )
