# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''Serves the public data API json and game client html using flask
for dynamic rendering of the content.
'''
from federation import app
from flask import json, render_template, request, make_response
from os import path, listdir

def _make_json(dictionary):
    '''Helper function that makes sure that the data served is
    recognized by browers as JSON.
    '''
    response = make_response(json.dumps(dictionary))
    response.mimetype = 'application/json'
    return response

def _get_header():
    '''Gets the custom HTML from templates/header.html, if it exists.
    '''
    template_path = path.join(path.dirname(__file__), 'templates')
    templates     = listdir(template_path)

    if 'header.html' in templates:
        header = open(path.join(template_path, 'header.html'), 'r')
        text   = header.read()

        header.close()
        return text

    else:
        return ''

def _check_login(login_data, user, password):
    '''Verifies the login information.
    '''
    if ('password' in login_data and 'user' in login_data and
        login_data['password'] == password and login_data['user'] == user):
        return True

    else:
        return False

def _check_cookie():
    '''Checks the cookie for the appropriate user.

    If there's no cookie, then the user is None.
    '''
    cookie = request.cookies.get('username')

    if cookie == 'michael':
        return True

    else:
        return False

def index():
    '''Serves as the main page when people visit the website.
    '''
    desc = 'Federation is a massively multiplayer turn based strategy game ' \
        'with a space setting. To play the game in your browser, visit '\
        '<a href="game.html">the game page</a>.'

    header = _get_header()

    return render_template('basic.html', body = desc, head = header)

def game():
    '''Creates an html page that uses javascript with canvas to format
    the main game board. This serves as a client built into the server
    so that downloading an external client is not required.
    '''
    canvases = ['header', 'board', 'sidebar', 'footer']
    scripts  = ['jquery.js', 'board.js', 'load.js', 'actions.js']

    html     = ''

    header   = _get_header()

    for canvas in canvases:
        html += '<canvas id="%s"></canvas> ' % canvas

    return render_template('basic.html', body=html,
                           javascript=scripts, head=header)

def login():
    '''Authenticates a user.
    '''
    status = {}

    user = 'michael'
    password = 'correcthorsebatterystaple'

    status['success'] = _check_login(request.form, user, password)

    response = _make_json(status)

    if status['success']:
        response.set_cookie('username', user)

    return response

def data_folder():
    '''Tells the client which pages to look for in the data directory
    for JSON information to parse.
    '''
    available = {}
    available['environment'] = True
    available['player']      = True

    available['secret'] = _check_cookie()

    return _make_json(available)

#### TODO: This is currently broken
def environment():
    '''Displays the public data from federation/data/environment in a
    way that the clients can parse using JSON.
    '''
    return _make_json(app.game.env.convert())

def players():
    '''Displays the username and IDs of all the players in the game.
    '''
    return _make_json(app.game.get_all_players())

def player(username):
    '''Displays the public stats of any given user.
    '''
    return _make_json(app.game.get_player(username))

def secret():
    '''This is a temporary test to show data to an authenticated user.
    '''
    if _check_cookie():
        return _make_json({'private' : 'Hello world!'})

    else:
        return _make_json({'restricted' : True})
