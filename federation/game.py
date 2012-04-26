# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

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

def get_all_players():
    '''Puts the player names and IDs in a dictionary.
    '''
    query = session.query(database.Player)
    users = query.all()
    names = {}

    for user in users:
        names[user.username] = user.id

    return names

def get_player(username):
    '''If the player is in the database, it returns the public
    data of the player in dictionary form.
    '''
    players = get_all_players()

    if username in players:
        query  = session.query(database.Player)
        player = query.filter(database.Player.username == username).first()

        return player.get_player_info()

    else:
        return {'Error' : '%s not found!' % (username) }
