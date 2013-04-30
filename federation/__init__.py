'''This package runs a Federation game server on top of SQLAlchemy,
Flask, and Avenue.

The server uses JSON as a client API. It also serves http pages that
can be accessed directly by a modern browser with JavaScript and
canvas support.
'''
from flask import Blueprint

app = Blueprint('federation', __name__,
                static_folder='static',
                url_prefix='/federation')

from federation import environment
from federation.database import database, session

def start():
    '''Sets up the game.
    '''
    environment.environment()
    database.debug()
