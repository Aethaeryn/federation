# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

from federation import environment, database

class Game():
    def __init__(self):
        environment.environment()

        database.debug()

    # Retrieves the player names and IDs in a processable format.
    def get_all_players(self):
        q     = database.session.query(database.Player)
        users = q.all()
        names = {}

        for user in users:
            names[user.username] = user.id

        return names

    def get_player(self, username):
        players = self.get_all_players()

        if username in players:
            q = database.session.query(database.Player)
            player = q.filter(database.Player.username == username).first()

            return player.get_player_info()

        else:
            return {'Error' : '%s not found!' % (username) }
