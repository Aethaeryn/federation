#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from server import environment, location, data, database
from copy import copy

# Contains the relevant player from the player table, and lists of things from
# other tables that have player as their 
class Player():
    def __init__(self, id):
        self.id = id
        self.load_from_db()

    # Reads in the data from the database matching the ID.
    def load_from_db(self):
        q = database.session.query(database.Player)

        self.__dict__.update(self.db_copy(q.filter(database.Player.id == self.id).first().__dict__))

        self.ships = self.has_id(database.Spacecraft, "owner")

        #### TODO: Also read in fleets and territory.

    def has_id(self, db, id_key):
        match_list = []

        q = database.session.query(db)

        matches = q.filter(db.__dict__[id_key] == self.id)

        for match in matches:
            match_list.append(self.db_copy(match.__dict__))

        return match_list

    def db_copy(self, db_return):
        dict_copy = copy(db_return)
        dict_copy.pop('_sa_instance_state')

        return dict_copy

    # Returns information that the GUI expects.
    def get_player_info(self):
        stats               = {}
        stats["name"]       = self.game_name
        stats["federation"] = self.federation
        stats["cash"]       = self.cash
        stats["income"]     = self.income
        stats["research"]   = self.research
        stats["ships"]      = len(self.ships)
        stats["fleets"]     = 1 #### fixme fleet_count
        stats["territory"]  = 2 #### fixme territory_count

        return stats


class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

        self.game = database.Game("Test", 2500, turns_per_day)

        self.debug()

    def debug(self):
        # Creates a dummy player to make sure the GUI can render player info.
        self.player = database.Player("michael", "Mike", "michael@example.com")
        self.player.cash = 20
        self.player.income = 2
        self.player.research = 4
        self.player.federation = "Empire"

        database.session.add(self.player)
        database.session.add(self.game)

        # Creates dummy spacecraft for the db.
        spaceships = ["Battle Frigate", "Battle Frigate", "Basic Fighter", "Cruiser"]

        for spaceship in spaceships:
            db_spaceship = database.Spacecraft(spaceship, "Foobar", " --- ", 1)
            database.session.add(db_spaceship)

        database.session.commit()

    # Retrieves the player data in a processable format.
    # Currently a messy hack to keep the UI working while the database is being written.
    def get_player_data(self):
         player_data = {}

         player_data["michael"] = Player(1).get_player_info()

         return player_data

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
