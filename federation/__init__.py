# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This package runs a Federation game server on top of SQLAlchemy,
Flask, and Avenue.

The server uses JSON as a client API. It also serves http pages that
can be accessed directly by a modern browser with JavaScript and
canvas support.
'''
from federation import public, game
from flask import Blueprint

class Federation():
    website = [['/'                       , 'game_index',  public.game_index],
               ['/data/'                  , 'data',        public.data_folder],
               ['/data/environment'       , 'environment', public.environment],
               ['/data/player/'           , 'players',     public.players],
               ['/data/player/<username>' , 'player',      public.player],
               ['/data/secret'            , 'secret',      public.secret]]

    def __init__(self):
        game.start()

app = Blueprint('fedgame', __name__, static_folder='static', url_prefix='/federation')

foo = Federation()

for page in foo.website:
    app.add_url_rule(*page)
