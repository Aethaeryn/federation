# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''Handles all of the Flask helper functions for public.py
'''
from flask import json, request, make_response, render_template

def make_json(dictionary):
    '''Helper function that makes sure that the data served is
    recognized by browers as JSON.
    '''
    response = make_response(json.dumps(dictionary))
    response.mimetype = 'application/json'
    return response

def check_login(login_data, user, password):
    '''Verifies the login information.
    '''
    if ('password' in login_data and 'user' in login_data and
        login_data['password'] == password and login_data['user'] == user):
        return True

    else:
        return False

def check_cookie():
    '''Checks the cookie for the appropriate user.

    If there's no cookie, then the user is None.
    '''
    cookie = request.cookies.get('username')

    if cookie == 'michael':
        return True

    else:
        return False

def make_page(**kwargs):
    return render_template('basic.html', **kwargs)
