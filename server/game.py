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

import environment, location, data

class GameObject():
    def __str__(self):
        return self.name

class Player(GameObject):
    def __init__(self, username, game_name, email, env):
        self.env       = env

        self.username  = username
        self.game_name = game_name
        self.email     = email
        self.join_date = data.getTime()

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

    def buyShip(self, ship, custom_name):
        self.addShip(self.env, ship, custom_name)
        self.cash -= ship.value

    def sellShip(self, ship):
        self.delShip(ship)
        self.cash += ship.value * 0.8

    def buyComponent(self, component, ship_id):
        self.ships[ship_id].addComponent(component)
        self.cash -= component.cost

    def sellComponent(self, comp_name, ship_id):
        self.ships[ship_id].sellComponent(comp_name)
        self.cash += self.env.obj["component"][comp_name].cost * 0.8

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
        self.date         = data.getTime()
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
    def __init__(self, turn_length):
        self.env = environment.Environment()

        self.sectors     = {}
        self.players     = {}
        self.alliance    = {}
        self.fleets      = {}
        self.turn        = 0
        self.turn_length = turn_length

        # fixme: Move into its own spot and call when necessary.
        self.json = data.WriteJSON('data')
        self.json.write('env', self.env.convert())

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

    def mainLoop(self):
        now = data.getTime()

        self.nextTurn(now)

        while True:
            now = data.getTime()

            if now - self.turn_time >= self.turn_length:
                self.nextTurn(now)

def main():
    game = Game(data.setTimeMinutes(100))

if __name__ == "__main__": main()
