#    Federation Server
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

# fixme: add buy/sell for structures/platforms/units
# fixme: add public-facing API

import core, environment, location
import datetime

class GameObject(core.CoreObject):
    # fixme: Redundant.
    def __str__(self):
        return self.name

# fixme: Handle authentication as well.
# fixme: Handle cash/income and last_view.
# fixme: Handle cases where not enough cash.
# fixme: Request membership in an alliance?
class Player(GameObject):
    def __init__(self, username, game_name, email, env):
        self.env       = env

        self.username  = username
        self.game_name = game_name
        self.email     = email
        self.join_date = datetime.datetime.now() # fixme, will not be in getStatus

        self.cash      = 0
        self.alliance  = False
        self.last_view = False

        self.ships     = {}

    def addShip(self, ship, custom_name):
        new_ship = self.env.get("spacecraft", ship)
        new_ship.custom_name = custom_name
        self.ships[new_ship.obj_id] = new_ship

    def delShip(self, ship):
        self.ships.pop(ship.obj_id)

    # fixme: Make possible only if chosen from shipyard.
    def buyShip(self, ship, custom_name):
        self.addShip(self.env, ship, custom_name)
        self.cash -= ship.value

    # fixme: Adjust selling value based on damage, too.
    def sellShip(self, ship):
        self.delShip(ship)
        self.cash += ship.value * 0.8

    # fixme: Make possible only if the ship is in friendly space.
    def buyComponent(self, component, ship_id):
        self.ships[ship_id].addExpansion(component)
        self.cash -= component.cost

    # fixme: Handle case where there's more than one component of the same name.
    # fixme: Adjust selling value based on damage, too.
    def sellComponent(self, comp_name, ship_id):
        self.ships[ship_id].sellExpansion(comp_name)
        self.cash += self.env.obj["component"][comp_name].cost * 0.8

    def renamePlayer(self, new_name):
        self.game_name = new_name

    def changeEmail(self, new_email):
        self.email = new_email

    def leaveAlliance(self):
        self.alliance = False

    def __str__(self):
        return self.username

# fixme: handle income, shared_view, and shared_fleet
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
        self.date         = datetime.datetime.now()
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

# fixme: add combat system
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

    # fixme: add movement
    def moveFleet(self):
        return "stub"

class Game():
    def __init__(self, turn_length):
        self.env = environment.Environment()

        self.sectors     = {}
        self.players     = {}
        self.alliance    = {}
        self.fleets      = {}
        self.turn        = 0
        self.turn_length = turn_length

        # self.mainLoop()

    def addPlayer(self, username, game_name, email):
        if username not in self.players:
            self.players[username] = Player(username, game_name, email, env)

    def addAlliance(self, name, founder):
        if name not in self.alliance:
            self.alliance[name] = Alliance(name, founder)

    def addSector(self, name):
        if name not in self.sectors:
            self.sectors[name] = location.Sector(self.env)

    def addFleet(self, name, player, ships):
        self.fleets[str(Fleet.fleet_counter)] = Fleet(name, player, ships)

    def delFleet(self, fleet_id):
        self.fleets.pop(str(fleet_id))

    def nextTurn(self, time):
        self.turn     += 1
        self.turn_time = time

        # TODO: Other things are done when turn is added, like refresh moves and update economic stuff.

    def getEnvData(self):
        return env.convert()

    def mainLoop(self):
        now = datetime.datetime.utcnow()

        self.nextTurn(now)

        # TODO: Listen for other things, like player-submitted moves.
        while True:
            now = datetime.datetime.utcnow()

            if now - self.turn_time >= self.turn_length:
                self.nextTurn(now)

def main():
    game = Game(datetime.timedelta(minutes=100))

if __name__ == "__main__": main()
