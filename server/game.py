#    Federation
#    Copyright (C) 2011 Michael Babich
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

import environment, location, data

class GameObject(object):
    def __str__(self):
        return self.name

class Player(GameObject):
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
    def getPlayerInfo(self):
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

    def addShip(self, ship, custom_name):
        new_ship = self.env.get("spacecraft", ship)
        new_ship.custom_name = custom_name
        self.ships[new_ship.obj_id] = new_ship

    def delShip(self, ship):
        self.ships.pop(ship.obj_id)

    def renamePlayer(self, new_name):
        self.game_name = new_name

    def changeEmail(self, new_email):
        self.email = new_email

    def leaveAlliance(self):
        self.alliance = False

    def __str__(self):
        return self.username

class Alliance(GameObject):
    def __init__(self, name, founder):
        # This holds the members.
        self.leaders      = {}
        self.members      = {}

        # Having the founder join the alliance.
        founder.alliance  = name

        # Various stats for the alliance.
        self.name         = name
        self.founder      = founder
        self.date         = data.Time.get()
        self.cash         = 0
        self.tax_rate     = 0
        self.shared_view  = False
        self.shared_fleet = False

        self.leaders[founder.username] = founder
        self.members[founder.username] = founder

    def addMember(self, player):
        self.members[player.username] = player
        player.alliance = self.name

    def removeMember(self, player):
        self.members.pop(player.username)
        player.leaveAlliance()

    def setTaxRate(self, rate):
        self.tax_rate = rate

    def setSharedView(self, toggle_view):
        self.shared_view = toggle_view

    def setSharedFleet(self, toggle_fleet):
        self.shared_fleet = toggle_fleet

class Fleet(GameObject):
    fleet_counter = 0

    def __init__(self, name, player, ships):
        self.fleet_id = self.fleet_counter
        Fleet.fleet_counter += 1

        self.ships   = {}
        self.players = {}

        self.ships[player.username]   = ships
        self.players[player.username] = player

        self.name      = name
        self.alliance  = player.alliance
        self.commander = player.username
        self.deputy    = None

    def addShip(self, ship):
        self.ships[ship.obj_id] = ship

    def delShip(self, ship):
        self.ships.pop(ship.obj_id)

class Game():
    def __init__(self, turns_per_day):
        self.env = environment.Environment()

        # These hold various data.
        self.sectors     = {}
        self.players     = {}
        self.alliance    = {}
        self.fleets      = {}

        # Keeps track of the turn.
        self.turn          = 0
        self.start_year    = 2500
        self.turns_per_day = turns_per_day

        # Runs actions.
        self.refreshEnvironmentData()
        self.mainLoop()

    # Writes env data to a publicly visible html page.
    def refreshEnvironmentData(self):
        self.out = data.Write('data')
        self.out.write('env', self.env.convert())

    def refreshLocationData(self, system):
        self.out = data.Write('data')
        self.out.write('loc', system.convert())

    # Adds a player.
    def addPlayer(self, username, game_name, email):
        if username not in self.players:
            self.players[username] = Player(username, game_name, email, env)

        else:
            raise Exception("A player with that username already exists!")

    # Transfers cash and research from one player to another.
    def transferFunds(self, original, target, amount_cash, amount_research):
        self.players[original].cash -= amount_cash
        self.players[target].cash   += amount_cash

        self.players[original].research -= amount_research
        self.players[target].research   += amount_research

    # Adds an alliance.
    def addAlliance(self, name, founder):
        if name not in self.alliance:
            self.alliance[name] = Alliance(name, founder)

        else:
            raise Exception("An alliance with that name already exists!")

    # Adds a sector.
    def addSector(self, name):
        if name not in self.sectors:
            self.sectors[name] = location.Sector(self.env, 40, 40)

        else:
            raise Exception("A sector with that name already exists!")

    # Adds a fleet.
    def addFleet(self, name, player, ships):
        self.fleets[str(Fleet.fleet_counter)] = Fleet(name, player, ships)

    # Deletes a fleet.
    def delFleet(self, fleet_id):
        return self.fleets.pop(str(fleet_id))

    # These events are called on every new turn.
    def nextTurn(self, time):
        self.turn     += 1
        self.turn_time = time

        #### Refresh unit move points and do queued actions.
        #### Update the economic income for player and alliance (including tax).
        #### Do other on-turn-start changes.

    # Turns the turn into a month and year.
    def getTurnDate(self):
        # Each month value is an index for months.
        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]

        # Every 12 turns is another year. Within a year, are 12 months.
        month = self.turn % 12
        year  = self.turn / 12

        year += self.start_year
        
        return months[month], year

    def mainLoop(self):
        now = data.Time.get()

        self.addSector("Test 1")

        self.refreshLocationData(self.sectors["Test 1"])

        #### Temporary debug thing. Remove me.
        quit()

        data.Time.setNextTurnEnd(self, self.turns_per_day)

        self.nextTurn(now)

        #### Listen for player-submitted moves/actions/combat/etc.

        while True:
            data.Time.sleep(.1)

            now = data.Time.get()

            if now >= self.turn_end:
                self.nextTurn(now)
                data.Time.setNextTurnEnd(self, self.turns_per_day)

def main():
    game = Game(1)

if __name__ == "__main__": main()
