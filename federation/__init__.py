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

app.game = game.Game()

public.login.methods = ['POST', 'GET']

app.add_url_rule('/', 'index', public.index)
app.add_url_rule('/game.html', 'game', public.game)
app.add_url_rule('/login', 'login', public.login)
app.add_url_rule('/data/', 'data', public.data_folder)
app.add_url_rule('/data/environment', 'environment', public.environment)
app.add_url_rule('/data/player/', 'players', public.players)
app.add_url_rule('/data/player/<username>', 'player', public.player)
app.add_url_rule('/data/secret', 'secret', public.secret)
