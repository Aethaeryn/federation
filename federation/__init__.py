# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This package runs a Federation game server on top of SQLAlchemy,
Flask, and Avenue.

The server uses JSON as a client API. It also serves http pages that
can be accessed directly by a modern browser with JavaScript and
canvas support.
'''
from flask import Blueprint

app = Blueprint('federation', __name__, static_folder='static', url_prefix='/federation')

from federation import public, game

game.start()
