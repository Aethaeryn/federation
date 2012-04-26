# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''The federation package contains everything that is necessary to run
a Federation game server.

It utilizes a SQL database using SQLAlchemy. It then presents public
data via Flask and WSGI. The server uses JSON as a client API. It also
serves http pages that can be accessed directly by a modern browser
with JavaScript and canvas support.
'''
from flask import Flask

app = Flask(__name__)

from federation import game, public

game.start()

def set_up():
    website = [['/'                       , 'index',       public.index],
               ['/data/'                  , 'data',        public.data_folder],
               ['/data/environment'       , 'environment', public.environment],
               ['/data/player/'           , 'players',     public.players],
               ['/data/player/<username>' , 'player',      public.player],
               ['/data/secret'            , 'secret',      public.secret]]

    for page in website:
        app.add_url_rule(*page)

set_up()
