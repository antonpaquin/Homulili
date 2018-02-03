from flask import request, redirect
from functools import wraps
import sqlite3
import argon2
import binascii
import os
import secrets
import logging

from common import render_template
from secret import auth_key
from config import user_database

logger = logging.getLogger(__name__)

conn = sqlite3.connect(user_database)


def hash_auth(uname, pass_hash):
    cur = conn.cursor()
    cur.execute('SELECT pass_hash FROM users WHERE username = ?', (uname,))
    results = cur.fetchone()
    cur.close()

    if not results:
        logger.warning('No such user {user}'.format(
            user=uname,
        ))
        return False

    hash = results[0]
    if hash != pass_hash:
        logger.warning('Invalid login for user {user}'.format(
            user=uname,
        ))
        return False

    logging.debug('Login successful')
    return True


def password_auth(uname, password):
    cur = conn.cursor()
    cur.execute('SELECT salt, pass_hash FROM users WHERE username = ?', (uname,))
    results = cur.fetchone()
    cur.close()

    if not results:
        logger.warning('No such user {user}'.format(
            user=uname,
        ))
        return False

    salt, stored_hash = results
    if not calculate_hash(password, salt) == stored_hash:
        logger.warning('Invalid login for user {user}'.format(
            user=uname,
        ))
        return False

    logging.debug('Login successful')
    return True


def login():
    logger.info('Responding to login request')
    uname = request.cookies.get('uname')
    password = request.args.get('password', '')

    if not password or not uname:
        logger.info('Incomplete login info')
        return render_template('login')

    if not valid_auth(uname, pass_hash):
        logger.info('Invalid login info: re-displaying login')
        return render_template('login')
    else:
        logger.info('Login complete, redirecting...')
        return redirect('/manga', code=302)


def authenticated(f):
    @wraps(f)
    def wrapped():
        logger.info('Checking authentication')
        uname = request.cookies.get('uname')
        pass_hash = request.cookies.get('pass_hash')
        if not pass_hash or not uname:
            logger.info('Incomplete auth, rejected')
            return '', 401

        if not hash_auth(uname, pass_hash):
            logger.info('Auth invalid, rejected')
            return '', 401

        else:
            logger.info('Auth OK')
            return f()

    return wrapped


def create_user(uname, password):
    salt = secrets.token_bytes(64)
    pass_hash = calculate_hash(password, salt)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, pass_hash, salt, api_key) VALUES (?, ?, ?, ?)',
                (uname, pass_hash, salt, ))


def calculate_hash(password, salt):
    return binascii.hexlify(argon2.argon2_hash(password, salt))

