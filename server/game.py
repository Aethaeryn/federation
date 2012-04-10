#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


from server import environment, location, data, database
from copy import copy

# Reads in a database table to a form recognized by Python and JSON.
# This prevents the same data from being stored in multiple locations in the db.
class ImportedObject():
    def __init__(self, id):
        self.id = id

    def is_id(self, db, use_id):
        q = database.session.query(db)

        return self.db_copy(q.filter(db.id == use_id).first())

    def has_id(self, db, id_key):
        q = database.session.query(db)

        matches = q.filter(db.__dict__[id_key] == self.id).all()

        for i in range(len(matches)):
            matches[i] = self.db_copy(matches[i])

        return matches

    def db_copy(self, db_item):
        dict_copy = copy(db_item.__dict__)
        dict_copy.pop('_sa_instance_state')

        return dict_copy

# Contains the relevant player from the player table, and lists of things from
# other tables that have this player mentioned.
class Player(ImportedObject):
    def __init__(self, id):
        ImportedObject.__init__(self, id)
        self.load_from_db()

    # Reads in the data from the database matching the ID.
    def load_from_db(self):
        self.__dict__.update(self.is_id(database.Player, self.id))

        self.federation = self.is_id(database.Federation, self.federation)['name']

        self.ships      = self.has_id(database.Spacecraft, "owner")
        self.fleets     = self.has_id(database.Fleet, "commander")

        #### TODO: Also read in territory.

    # Returns information that the GUI expects.
    def get_player_info(self):
        #### Temporary, remove me when it works!
        self.territory = [None, None]

        stats               = {}
        stats["name"]       = self.game_name
        stats["federation"] = self.federation
        stats["cash"]       = self.cash
        stats["income"]     = self.income
        stats["research"]   = self.research
        stats["ships"]      = len(self.ships)
        stats["fleets"]     = len(self.fleets)
        stats["territory"]  = len(self.territory)

        return stats

class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

        self.game = database.Game("Test", 2500, turns_per_day)

        self.debug()

    def debug(self):
        # Player
        self.player = database.Player("michael", "Mike", "michael@example.com")
        self.player.cash = 20
        self.player.income = 2
        self.player.research = 4
        self.player.federation = 1

        database.session.add(self.player)
        database.session.add(self.game)

        # Spacecraft
        spaceships = ["Battle Frigate", "Battle Frigate", "Basic Fighter", "Cruiser"]

        for spaceship in spaceships:
            db_spaceship = database.Spacecraft(spaceship, "Foobar", " --- ", 1)
            database.session.add(db_spaceship)

        # Fleet
        database.session.add(database.Fleet("Zombie Raptor", 1))

        # Federation
        database.session.add(database.Federation("Empire", 1))

        # Component
        database.session.add(database.Component("Small Hull", 3))

        # This must come last!
        database.session.commit()

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
            return Player(players[username]).get_player_info()

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
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"]

        # Every 12 turns is another year. Within a year, are 12 months.
        month = self.game.turn % 12
        year  = self.game.turn / 12

        year += self.game.start_year

        return months[month], year
