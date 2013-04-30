'''This file runs a game server of Federation by acting as an
intermediary between the web server and the database.
'''
from federation import environment
from federation.database import database, session

def start():
    '''Sets up the game.
    '''
    environment.environment()
    database.debug()
