#!/usr/bin/env python

import httplib2
from json import loads
from oauth2client.client import verify_id_token
from oauth2client.crypt import AppIdentityError
from flask import Blueprint, render_template, flash, request, session, abort,\
    json, redirect, url_for
from blueprints import db
from models import User
import utilities

mod = Blueprint('user', __name__, template_folder='templates')


# All routes prefixed with /user

@mod.route('/login/')
def login():

    # Setup CSRF protection
    state = utilities.get_state()
    session['state'] = state
    return render_template('login.html.j2', state=state, page='Login')


@mod.route('/gconnect', methods=['POST'])
def gconnect():
    data = request.get_json()

    # CSRF protection
    if u'state' not in data or u'state' not in session or \
            data[u'state'] != session[u'state']:
        abort(401)
    code = data[u'code']
    try:

        # Check google token valididity
        result = verify_id_token(code,
        '201339145304-jp8b9vd0od27pcsma7ke52jsol7gdd6u.apps.googleusercontent.com')  # NOQA: E501
        if result['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise AppIdentityError('wrong issuer')
    except AppIdentityError:
        abort(401)
    try:

        #  try to find user record
        active_user = User.by_google_uuid(result['sub'])
        assert active_user is not None
    except:

        #  if no user, add new user to db
        uuid = result['sub']
        email = result['email']
        name = result['name']
        active_user = User(uuid, email, 'google', name)
        db.session.add(active_user)
        db.session.commit()

    # Login success. Set session and redirect
    flash('You are now logged in', 'success')
    session['logged_in'] = True
    session['user'] = active_user.id
    del session['state']
    # Redirect handled in js after any 200-299 response
    return json.jsonify(success=True)


@mod.route('/fbconnect', methods=['POST'])
def fbconnect():
    data = request.get_json()

    # CSRF protection
    if 'state' not in data or 'state' not in session or\
            session['state'] != data['state']:
        abort(401)
    # Check if token is valid
    h = httplib2.Http()
    valid_token = h.request('https://graph.facebook.com/debug_token?input_token={0}&access_token=140367659868833|a108883439cabf0784953a3ab504c60a'  # NOQA: E501
                            .format(data['code']))
    valid_token = loads(valid_token[1])['data']
    # Check if token is for this app
    if valid_token[u'app_id'] != '140367659868833'\
            or not valid_token['is_valid']:
        abort(401)
    # Get user data
    user_data = h.request('https://graph.facebook.com/me?fields=email,name&access_token={0}'  # NOQA: E501
                          .format(data['code']))
    user_data = loads(user_data[1])
    uuid = user_data[u'id']
    try:
        # Search for user in db
        user = User.by_facebook_uuid(uuid)
        assert user is not None
    except:
        # If no user, add to db
        # fb seems to replace @ with its unicode \u0040
        email = user_data[u'email'].replace('\u0040', '@')
        name = user_data[u'name']
        user = User(uuid, email, 'facebook', name)
        db.session.add(user)
        db.session.commit()

    # Set session and redirect
    flash('You are now logged in', 'success')
    session['logged_in'] = True
    session['user'] = user.id
    del session['state']
    # Redirect handled in js after any 200-299 response
    return json.jsonify(success=True)


@mod.route('/logout/')
@utilities.login_required
def logout():
    # Kill session
    del session['logged_in']
    del session['user']
    flash('You have successfully logged out', 'success')
    return redirect(url_for('home'))
