from flask import request, redirect
import hashlib
from functools import wraps
import logging

from common import render_template
from secret import auth_key

logger = logging.getLogger(__name__)


def login():
    logger.info('Responding to login request')
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    if not token or not uname:
        logger.info('No login info set')
        return render_template('login')

    md5 = hashlib.md5()
    md5.update(uname.encode('utf-8'))
    md5.update(auth_key.encode('utf-8'))
    digest = md5.hexdigest()

    if digest != token:
        logger.info('Invalid login info: re-displaying login')
        return render_template('login')

    else:
        logger.info('Login is already present, redirecting...')
        return redirect('/manga', code=302)


def authenticated(f):
    @wraps(f)
    def wrapped():
        logger.info('Checking authentication')
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        if not token or not uname:
            logger.info('No auth present, rejected')
            return '', 401

        md5 = hashlib.md5()
        md5.update(uname.encode('utf-8'))
        md5.update(auth_key.encode('utf-8'))
        digest = md5.hexdigest()

        if digest != token:
            logger.info('Auth invalid, rejected')
            return '', 401

        else:
            logger.info('Auth OK')
            return f()

    return wrapped

