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

import core
import random

# Stores environmental objects at a given location.
# Provides certain algorithms for hex board calculations.
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.fleets = set([])
        self.body   = False

    def __str__(self):
        return "(%2s, %2s)" % (str(self.x), str(self.y))

    # Calculates distance on a hex board.
    def distance(self, location):
        horizontal = abs(self.x - location.x)

        penalty = 0

        if (((self.x % 2) and not (location.x % 2) and self.y < location.y)
            or (location.x % 2) and not (self.x % 2) and location.y < self.y):
            penalty = 1

        alt_distance = abs(self.y - location.y) + penalty + (horizontal / 2)

        return max(horizontal, alt_distance)

    # Returns a set of tuple (x, y) coordinates in the radius range.
    def radius(self, radius):
        radius_set = set([])

        # Case 1: The radius is even.
        if not radius % 2:

            # Generates the left side of the hex range.
            for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
                radius_set.add((self.x - radius, self.y + i))

            # Generates the right side of the hex range
            for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
                radius_set.add((self.x + radius, self.y + i))

            # Connects the corners on the other sides.
            y1  = self.y - radius
            y2  = self.y + radius
            x1  = self.x
            x2  = self.x

            for i in range(radius):
                radius_set.add((x1, y1))
                radius_set.add((x2, y1))
                radius_set.add((x1, y2))
                radius_set.add((x2, y2))

                # Odds walk the hexes a certain way.
                if x1 % 2:
                    x1 -= 1
                    x2 += 1
                    y2 -= 1

                # Evens walk the hexes another way.
                else:
                    x1 -= 1
                    x2 += 1
                    y1 += 1

        return radius_set

    def addBody(self, body):
        if not self.body:
            self.body = body

        else:
            raise Exception("Body already exists at location!")

    def addFleet(self, fleet):
        self.fleets.add(fleet)

    def removeFleet(self, fleet):
        if fleet in self.fleets:
            self.fleets.remove(fleet)

        else:
            raise Exception("Fleet does not exist at location!")

# Holds locations of significance.
class Map(core.CoreObject):
    name = "Map"

    # Creates a map with given x, y size limits.
    def __init__(self, x, y):
        self.map = {}
        self.x   = x
        self.y   = y

    # Accesses coordinates at a given location.
    def accessCoords(self, x, y):
        location_key = "%3i, %3i" % (x, y)

        # If this is the first access, it creates a new Location object.
        if location_key not in self.map:
            self.map[location_key] = Location(x, y)

        return self.map[location_key]

    # Lists all coordinates.
    def list(self):
        ls = ""

        for location_key in sorted(self.map.keys()):
            location = self.map[location_key]

            if location.body:
                ls += "%s %s\n" % (location, location.body)

        return ls[:-1]

    def __str__(self):
        if self.name == "Star":
            return self.longInfo()

        else:
            return self.name

class Tactical(Map):
    def __init__(self, env):
        self.env = env

        self.size = (40, 40)

        Map.__init__(self, self.size[0], self.size[1])

# Holds the large environmental objects in a star system.
class System(Map):
    def __init__(self, env):
        self.env  = env

        # Random size/name of star system.
        self.name = "Star"
        self.size = (random.randint(60, 70), random.randint(60, 70))

        Map.__init__(self, self.size[0], self.size[1])

        self.typeZeroSystem()

    # A type zero star system has a star at the center and looks like our system.
    # This is being used for debug purposes.
    def typeZeroSystem(self):
        center = ((self.size[0] - 1) / 2, (self.size[1] - 1) / 2)

        star     = self.env.get("body", "Star")
        planet   = self.env.get("body", "Planet")
        asteroid = self.env.get("body", "Asteroid Field")

        self.accessCoords(center[0], center[1]).addBody(star)
        
        distances = [1, 2, 3, 4, 9, 15, 21, 27]

        # The planets start in x alignment with each other.
        for distance in distances:
            self.accessCoords(center[0], center[1] + distance).addBody(planet)

        # Use radius to generate belt instead.

        # belt_distance = 6
        # self.accessCoords(center[0], center[1] + belt_distance).addBody(asteroid)
        # self.accessCoords(center[0], center[1] + belt_distance + 1).addBody(asteroid)

    def longInfo(self):
        return "%s System %3i x %3i" % (self.name, self.size[0], self.size[1])

# Holds star systems.
class Sector(Map):
    # Creates a star sector with an environment.py instance, and a max x and y.
    def __init__(self, env, x, y):
        Map.__init__(self, x, y)
        
        self.env    = env

        self.generateSector()
        self.name = "Sector"

    # Places stars randomly in the map.
    def generateSector(self):
        for i in range(self.x * self.y / 5):
            coords = (random.randint(0, self.x - 1), random.randint(0, self.y - 1))

            if not self.accessCoords(coords[0], coords[1]).body:
                self.accessCoords(coords[0], coords[1]).addBody(System(self.env))
