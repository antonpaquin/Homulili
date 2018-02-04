import sqlite3
import argon2
import binascii
import secrets

from flask import request, redirect
from functools import wraps
import logging

import backend
from common import render_template
from config import user_database

logger = logging.getLogger(__name__)

conn = sqlite3.connect(user_database)


def login():
    logger.info('Responding to login')
    return render_template('login')


def login_target():
    logger.info('Responding to login::login')

    uname = request.form.get('uname', None)
    password = request.form.get('password', None)

    if not uname or not password:
        logger.info('Incomplete login info')
        return '', 400

    auth, pass_hash = password_auth(uname, password)
    if not auth:
        logger.info('Invalid login info')
        return '', 401
    else:
        logger.info('Login complete')
        return pass_hash, 200


def create_target():
    logger.info('Responding to login::create')

    uname = request.form.get('uname', None)
    password = request.form.get('password', None)

    if not uname or not password:
        logger.info('Incomplete user::create info')
        return '', 400

    created, pass_hash = create_user(uname, password)
    if not created:
        logger.warning('Failed to create user')
        return '', 400
    else:
        logger.info('Created user {name}'.format(
            name=uname,
        ))
        return pass_hash, 200


def authenticated(f):
    @wraps(f)
    def wrapped():
        logger.info('Checking authentication')
        uname = request.cookies.get('uname')
        pass_hash = request.cookies.get('pass_hash')
        if not pass_hash or not uname:
            logger.info('Incomplete auth, rejected')
            return '', 401

        auth, api_key = hash_auth(uname, pass_hash)
        if not auth:
            logger.info('Auth invalid, rejected')
            return '', 401

        else:
            logger.info('Auth OK')
            return f(api_key)

    return wrapped


def create_user(uname, password):
    salt = binascii.hexlify(secrets.token_bytes(64))
    pass_hash = calculate_hash(password, salt)

    if user_exists(uname):
        return False, None

    try:
        api_key = backend.admin.create(p_read=True, p_index=True)['new_key']
    except KeyError:
        logger.error('Backend failed to generate api key')
        return False, None

    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, pass_hash, salt, api_key) VALUES (?, ?, ?, ?)',
                    (uname, pass_hash, salt, api_key))
    except Exception as e:
        logger.error('Exception in create user: {err}'.format(
            err=str(e),
        ))
        conn.rollback()
        return False, None

    conn.commit()
    return True, pass_hash


def user_exists(uname):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (uname,))
    results = cur.fetchone()
    return bool(results)


def calculate_hash(password, salt):
    return binascii.hexlify(argon2.argon2_hash(password, salt))


def hash_auth(uname, pass_hash):
    logger.info('Entering hash_auth')

    cur = conn.cursor()
    cur.execute('SELECT pass_hash, api_key FROM users WHERE username = ?', (uname,))
    results = cur.fetchone()
    cur.close()

    if not results:
        logger.warning('No such user {user}'.format(
            user=uname,
        ))
        return False, None

    test_hash = results[0].decode('utf-8')
    if test_hash != pass_hash:
        logger.warning('Invalid login for user {user};'.format(
            user=uname,
        ))
        return False, None

    api_key = results[1]

    logger.debug('Login successful')
    return True, api_key


def password_auth(uname, password):
    logger.info('Entering password_auth')

    cur = conn.cursor()
    cur.execute('SELECT salt, pass_hash FROM users WHERE username = ?', (uname,))
    results = cur.fetchone()
    cur.close()

    if not results:
        logger.warning('No such user {user}'.format(
            user=uname,
        ))
        return False, None

    salt, stored_hash = results
    test_hash = calculate_hash(password, salt)
    if not test_hash == stored_hash:
        logger.warning('Invalid login for user {user}'.format(
            user=uname,
        ))
        return False, None

    logger.debug('Login successful')
    return True, test_hash
