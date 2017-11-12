from flask import request, redirect
import hashlib
from functools import wraps

from common import render_template
from secret import auth_key


def login():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    if not token or not uname:
        return render_template('login')

    md5 = hashlib.md5()
    md5.update(uname.encode('utf-8'))
    md5.update(auth_key.encode('utf-8'))
    digest = md5.hexdigest()

    if digest != token:
        return render_template('login')

    else:
        return redirect('/manga', code=302)


def authenticated(f):
    @wraps(f)
    def wrapped():
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        if not token or not uname:
            return '', 401

        md5 = hashlib.md5()
        md5.update(uname.encode('utf-8'))
        md5.update(auth_key.encode('utf-8'))
        digest = md5.hexdigest()

        if digest != token:
            return '', 401

        else:
            return f()

    return wrapped

