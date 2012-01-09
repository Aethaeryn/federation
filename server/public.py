#    Federation
#    Copyright (C) 2011 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Serves the public data API json and game client html using flask for
dynamic rendering of the content.
"""

from server import app
from flask import json, render_template, request, make_response
from os import path

# *** Index page
@app.route('/')
def index():
    """Serves as the main page that greets people when they visit the website.
    """
    desc = 'Federation is a massively multiplayer turn based strategy game with a space setting. To play the game in your browser, visit <a href="game.html">the game page</a>.'

    return render_template('basic.html', body = desc)

@app.route('/index.html')
def index2():
    """Points to the index page at '/' for compatability reasons.
    """
    return index()


# *** Authentication and authenticated actions.
@app.route('/login', methods=['POST', 'GET'])
def login():
    """Authenticates a user.
    """
    status = {}

    user = 'michael'
    password = 'correcthorsebatterystaple'

    status['success'] = check_login(request.form, user, password)

    response = make_response(json.dumps(status))

    if status['success']:
        response.set_cookie('username', user)

    return response

@app.route('/move', methods=['POST', 'GET'])
def move():
    """Sends a game move to the game server.
    """

    moves = request.form

    status = {}

    status['success'] = check_cookie()

    return json.dumps(status)

def check_login(data, user, password):
    """Verifies the login information.
    """
    if ('password' in data and 'user' in data and
        data['password'] == password and data['user'] == user):
        return True

    else:
        return False

def check_cookie():
    """Checks the cookie for the appropriate user.
    """
    # If no cookie, the user is None
    cookie = request.cookies.get('username')

    if cookie == 'michael':
        return True

    else:
        return False


# *** Retrieve JSON data
@app.route('/data/')
def data():
    """Tells the client which pages to look for in the data directory for
    JSON information to parse.
    """
    available = {}
    available["environment"] = True

    available["secret"] = check_cookie()

    return json.dumps(available)

@app.route('/data/environment')
def environment():
    """Displays the public data from server/data/environment in a way that
    the clients can parse using JSON.
    """
    return json.dumps(app.game.env.convert())

@app.route('/data/secret')
def secret():
    """This is a temporary test to show data only to an authenticated user.
    """
    if check_cookie():
        return json.dumps({'private' : 'Hello world!'})
    
    else:
        return json.dumps({'restricted' : True}), 403

# @app.route('/data/location')
# def loc():
#     return json.dumps(app.game.system.convert())


# *** Play the game
@app.route('/game.html')
def game():
    """Creates an html page that uses javascript with canvas to format the
    main game board. This serves as a client built into the server so that
    downloading an external client is not required.
    """
    canvases = ['header', 'board', 'sidebar', 'footer']
    html     = ''

    for canvas in canvases:
        html += '<canvas id="%s"></canvas> ' % canvas

    return render_template('basic.html', body = html, javascript = 'board.js')

