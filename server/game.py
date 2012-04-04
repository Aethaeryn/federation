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

class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

        # Keeps track of the turn.
        self.turn          = 0
        self.start_year    = 2500
        self.turns_per_day = turns_per_day

        # Creates a dummy player to make sure the GUI can render player info.
        self.player = database.Player("michael", "Mike", "michael@example.com")
        self.player.cash = 20
        self.player.income = 2
        self.player.research = 4
        self.player.federation = "Empire"

        database.session.add(self.player)
        database.session.commit()

    # Retrieves the player data in a processable format.
    # Currently a messy hack to keep the UI working while the database is being written.
    def get_player_data(self):
         player_data = {}

         player_data["michael"] = self.player.get_player_info()

         return player_data

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
        #### Update the economic income for player and federation (including tax).
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
