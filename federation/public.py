'''Serves the public data API json and game client html using flask
for dynamic rendering of the content.
'''
from federation import game, app
from avenue import api

@app.route('/')
def game_index():
    '''Creates an html page that uses javascript with canvas to format
    the main game board. This serves as a client built into the server
    so that downloading an external client is not required.
    '''
    canvases = ['header', 'board', 'sidebar', 'footer']
    scripts  = ['jquery.js', 'board.js', 'load.js', 'actions.js']

    html     = ''

    header   = api.get_header()

    for canvas in canvases:
        html += '<canvas id="%s"></canvas> ' % canvas

    return api.make_page(body=html, javascript=scripts, head=header,
                         style='../static/dark-plain')

@app.route('/data/')
def data_folder():
    '''Tells the client which pages to look for in the data directory
    for JSON information to parse.
    '''
    available = {}
    available['environment'] = True
    available['player']      = True
    available['secret']      = api.check_cookie()

    return api.make_json(available)

#### TODO: This is currently broken
@app.route('/data/environment')
def environment():
    '''Displays the public data from federation/data/environment in a
    way that the clients can parse using JSON.
    '''
    return api.make_json(game.env.convert())

@app.route('/data/player/')
def players():
    '''Displays the username and IDs of all the players in the game.
    '''
    return api.make_json(game.get_all_players())

@app.route('/data/player/<username>')
def player(username):
    '''Displays the public stats of any given user.
    '''
    return api.make_json(game.get_player(username))

@app.route('/data/secret')
def secret():
    '''This is a temporary test to show data to an authenticated user.
    '''
    if api.check_cookie():
        return api.make_json({'private' : 'Hello world!'})

    else:
        return api.make_json({'restricted' : True})
