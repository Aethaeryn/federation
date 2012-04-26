# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''The federation package contains everything that is necessary to run
a Federation game server.

It utilizes a SQL database using SQLAlchemy. It then presents public
data via Flask and WSGI. The server uses JSON as a client API. It also
serves http pages that can be accessed directly by a modern browser
with JavaScript and canvas support.
'''
from federation import public, game

class Federation():
    website = [['/'                       , 'game_index',  public.game_index],
               ['/data/'                  , 'data',        public.data_folder],
               ['/data/environment'       , 'environment', public.environment],
               ['/data/player/'           , 'players',     public.players],
               ['/data/player/<username>' , 'player',      public.player],
               ['/data/secret'            , 'secret',      public.secret]]

    def __init__(self):
        game.start()
