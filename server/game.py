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

class Player(object):
    def __init__(self, username, game_name, email, env):
        self.env       = env

        self.username  = username
        self.game_name = game_name
        self.email     = email
        self.join_date = data.Time.get()

        self.cash      = 0
        self.income    = 0
        self.research  = 0
        self.alliance  = False

        self.ships     = {}

        self.fleet_count     = 0
        self.territory_count = 0

    # Returns information the GUI expects.
    def get_player_info(self):
        stats = {}
        stats["name"]       = self.game_name
        stats["federation"] = self.alliance
        stats["cash"]       = self.cash
        stats["income"]     = self.income
        stats["research"]   = self.research
        stats["ships"]      = len(self.ships)
        stats["fleets"]     = self.fleet_count
        stats["territory"]  = self.territory_count

        return stats

class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

        # These hold various data.
        self.players     = {}

        # Keeps track of the turn.
        self.turn          = 0
        self.start_year    = 2500
        self.turns_per_day = turns_per_day

        # Creates a dummy player to make sure the GUI can render player info.
        self.add_player("michael", "Mike", "michael@example.com")
        self.players["michael"].cash = 20
        self.players["michael"].income = 2
        self.players["michael"].research = 4
        self.players["michael"].alliance = "Empire"
        self.players["michael"].ships = [None, None, None, None]
        self.players["michael"].fleet_count = 1
        self.players["michael"].territory_count = 2

    # Retrieves the player data in a processable format.
    def get_player_data(self):
         player_data = {}

         for player in self.players:
             player_data[player] = self.players[player].get_player_info()

         return player_data

    # Adds a player.
    def add_player(self, username, game_name, email):
        if username not in self.players:
            self.players[username] = Player(username, game_name,
                                            email, self.env)

        else:
            raise Exception("A player with that username already exists!")

    # Transfers cash and research from one player to another.
    def transfer_funds(self, original, target, amount_cash, amount_research):
        self.players[original].cash -= amount_cash
        self.players[target].cash   += amount_cash

        self.players[original].research -= amount_research
        self.players[target].research   += amount_research

    # These events are called on every new turn.
    def next_turn(self, time):
        self.turn     += 1
        self.turn_time = time

        #### Refresh unit move points and do queued actions.
        #### Update the economic income for player and alliance (including tax).
        #### Do other on-turn-start changes.

    # Turns the turn into a month and year.
    def get_turn_date(self):
        # Each month value is an index for months.
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December"]

        # Every 12 turns is another year. Within a year, are 12 months.
        month = self.turn % 12
        year  = self.turn / 12

        year += self.start_year
        
        return months[month], year
