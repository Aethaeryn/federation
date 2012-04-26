# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''Serves the public data API json and game client html using flask
for dynamic rendering of the content.
'''
from federation import game
from avenue.api import *
from os import path, listdir

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

def game_index():
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

    return make_page(body=html, javascript=scripts, head=header)

def data_folder():
    '''Tells the client which pages to look for in the data directory
    for JSON information to parse.
    '''
    available = {}
    available['environment'] = True
    available['player']      = True

    available['secret'] = check_cookie()

    return make_json(available)

#### TODO: This is currently broken
def environment():
    '''Displays the public data from federation/data/environment in a
    way that the clients can parse using JSON.
    '''
    return make_json(game.env.convert())

def players():
    '''Displays the username and IDs of all the players in the game.
    '''
    return make_json(game.get_all_players())

def player(username):
    '''Displays the public stats of any given user.
    '''
    return make_json(game.get_player(username))

def secret():
    '''This is a temporary test to show data to an authenticated user.
    '''
    if check_cookie():
        return make_json({'private' : 'Hello world!'})

    else:
        return make_json({'restricted' : True})
