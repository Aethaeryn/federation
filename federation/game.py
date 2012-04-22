# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

'''This file runs a game server of Federation by acting as an
intermediary between the web server and the database.
'''
from federation import environment
from federation.database import database

class Game():
    '''Acts as an instance of a game server. Multiple games are
    planned to eventually be able to run at the same time next to each
    other so that different games running different settings can run
    on the same Federation server.
    '''
    def __init__(self):
        '''Sets up the game.
        '''
        environment.environment()
        database.debug()

    def get_all_players(self):
        '''Puts the player names and IDs in a dictionary.
        '''
        query = database.session.query(database.Player)
        users = query.all()
        names = {}

        for user in users:
            names[user.username] = user.id

        return names

    def get_player(self, username):
        '''If the player is in the database, it returns the public
        data of the player in dictionary form.
        '''
        players = self.get_all_players()

        if username in players:
            query  = database.session.query(database.Player)
            player = query.filter(database.Player.username == username).first()

            return player.get_player_info()

        else:
            return {'Error' : '%s not found!' % (username) }
