#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


"""Serves the public data API json and game client html using flask
for dynamic rendering of the content.
"""

from federation import app, data
from flask import json, render_template, request, make_response

# *** Helper functions.
def make_json(dictionary):
    """Helper function that makes sure that the data served is
    recognized by browers as JSON.
    """
    response = make_response(json.dumps(dictionary))
    response.mimetype = 'application/json'
    return response


# *** Index page
@app.route('/')
def index():
    """Serves as the main page when people visit the website.
    """
    desc = 'Federation is a massively multiplayer turn based strategy game with '\
        'a space setting. To play the game in your browser, visit '\
        '<a href="game.html">the game page</a>.'

    header = data.parse_header()

    return render_template('basic.html', body = desc, head = header)


# *** Authentication and authenticated actions.
@app.route('/login', methods=['POST', 'GET'])
def login():
    """Authenticates a user.
    """
    status = {}

    user = 'michael'
    password = 'correcthorsebatterystaple'

    status['success'] = check_login(request.form, user, password)

    response = make_json(status)

    if status['success']:
        response.set_cookie('username', user)

    return response

#### Fixme: This doesn't currently do anything.
@app.route('/move', methods=['POST', 'GET'])
def move():
    """Sends a game move to the game server.
    """
    moves = request.form

    status = {}

    status['success'] = check_cookie()

    return make_json(status)

def check_login(login_data, user, password):
    """Verifies the login information.
    """
    if ('password' in login_data and 'user' in login_data and
        login_data['password'] == password and login_data['user'] == user):
        return True

    else:
        return False

def check_cookie():
    """Checks the cookie for the appropriate user.

    If there's no cookie, then the user is None.
    """
    cookie = request.cookies.get('username')

    if cookie == 'michael':
        return True

    else:
        return False


# *** Retrieve JSON data
@app.route('/data/')
def data_folder():
    """Tells the client which pages to look for in the data directory
    for JSON information to parse.
    """
    available = {}
    available['environment'] = True
    available['player']      = True

    available['secret'] = check_cookie()

    return make_json(available)

@app.route('/data/environment')
def environment():
    """Displays the public data from federation/data/environment in a
    way that the clients can parse using JSON.
    """
    return make_json(app.game.env.convert())

@app.route('/data/player/')
def players():
    """Displays the username and IDs of all the players in the game.
    """
    return make_json(app.game.get_all_players())

@app.route('/data/player/<username>')
def player(username):
    """Displays the public stats of any given user.
    """
    return make_json(app.game.get_player(username))

@app.route('/data/secret')
def secret():
    """This is a temporary test to show data to an authenticated user.
    """
    if check_cookie():
        return make_json({'private' : 'Hello world!'})

    else:
        return make_json({'restricted' : True})


# *** Play the game
@app.route('/game.html')
def game():
    """Creates an html page that uses javascript with canvas to format
    the main game board. This serves as a client built into the server
    so that downloading an external client is not required.
    """
    canvases = ['header', 'board', 'sidebar', 'footer']
    scripts  = ['jquery.js', 'board.js', 'load.js', 'actions.js']

    html     = ''

    header   = data.parse_header()

    for canvas in canvases:
        html += '<canvas id="%s"></canvas> ' % canvas

    return render_template('basic.html', body = html, javascript = scripts, head = header)
