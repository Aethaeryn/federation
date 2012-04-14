#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


from server import environment, location, data, database
from copy import copy

class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

#        self.game = database.Game('Test', 2500, turns_per_day)

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

    # These events are called on every new turn.
    def next_turn(self, time):
        pass

        #### Increment the turn by one.
        #### Mark the time of the turn.
        #### Refresh unit move points and do queued actions.
        #### Update the economic income for player and federation (including tax).
        #### Do other on-turn-start changes.

    # Turns the turn into a month and year.
    def get_turn_date(self):
        # Each month value is an index for months.
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']

        # Every 12 turns is another year. Within a year, are 12 months.
        month = self.game.turn % 12
        year  = self.game.turn / 12

        year += self.game.start_year

        return months[month], year
