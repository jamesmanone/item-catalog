import random
import string
from flask import json, make_response, redirect, url_for, session, flash
from functools import wraps


def get_state():
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for x in xrange(32))


def make_cors_json_response(data):
    res = make_response(json.jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


def login_required(fx):
    @wraps(fx)
    def wrapper(*args, **kwargs):
        if not session or 'user' not in session:
            flash('You must be logged in to do that', 'danger')
            return redirect(url_for('user.login'))
        else:
            return fx(*args, **kwargs)
    return wrapper
