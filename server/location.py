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

import random, copy

# Stores environmental objects at a given location.
# Provides certain algorithms for hex board calculations.
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

# Holds locations of significance.
class Map():
    name = "Map"

    # Creates a map with given x, y size limits.
    def __init__(self, x, y):
        self.map = {}
        self.x   = x
        self.y   = y

    def setCoords(self, x, y, body):
        location_key = "%3i, %3i" % (x, y)

        self.map[location_key] = body

    def delCoords(self, x, y, body):
        location_key = "%3i, %3i" % (x, y)

        try:
            return self.map.pop(location_key)

        except KeyError:
            return None

    def convert(self):
        converted = copy.copy(self.__dict__)

        if hasattr(self, "body"):
            converted["body"] = converted["body"].__dict__

        converted.pop("env")

        # If there's a convert method, use it instead of a dictionary.
        for location in converted["map"]:
            if hasattr(converted["map"][location], "convert"):
                converted["map"][location] = converted["map"][location].convert()

            else:
                converted["map"][location] = converted["map"][location].__dict__

        return converted

class Tactical(Map):
    # Planet or asteroid field.
    def __init__(self, env, body):
        self.env  = env
        self.body = body
        self.name = self.body.name

        self.size = (40, 40)

        Map.__init__(self, self.size[0], self.size[1])

        center = ((self.size[0] - 1) / 2, (self.size[1] - 1) / 2)

        self.setCoords(center[0], center[1], self.body)

        # Generator goes here.

# Holds the large environmental objects in a star system.
class System(Map):
    def __init__(self, env):
        self.env  = env

        # Random size/name of star system.
        self.name = "Star"
        # self.size = (random.randint(60, 70), random.randint(60, 70))
        self.size = (40, 40)

        Map.__init__(self, self.size[0], self.size[1])

        self.typeZeroSystem()

    # A type zero star system has a star at the center and looks like our system.
    # This is being used for debug purposes.
    def typeZeroSystem(self):
        center = ((self.size[0] - 1) / 2, (self.size[1] - 1) / 2)

        star     = self.env.get("body", "Star")
        planet   = self.env.get("body", "Planet")
        asteroid = self.env.get("body", "Asteroid Field")

        self.setCoords(center[0], center[1], star)

        distances = [1, 2, 3, 4, 8, 11, 14, 17]

        # The planets start in x alignment with each other.
        for distance in distances:
            self.setCoords(center[0], center[1] + distance, Tactical(self.env, planet))

        # Use radius to generate belt instead.

        # belt_distance = 6
        # self.accessCoords(center[0], center[1] + belt_distance).addBody(Tactical(self.env, asteroid))
        # self.accessCoords(center[0], center[1] + belt_distance + 1).addBody(Tactical(self.env, asteroid))

    def longInfo(self):
        return "%s System %3i x %3i" % (self.name, self.size[0], self.size[1])

# Holds star systems.
class Sector(Map):
    # Creates a star sector with an environment.py instance, and a max x and y.
    def __init__(self, env, x, y):
        Map.__init__(self, x, y)
        
        self.env    = env

        # self.generateSector()

        self.setCoords(0, 0, System(self.env))

        self.name = "Sector"

    # Places stars randomly in the map.
    def generateSector(self):
        for i in range(self.x * self.y / 5):
            coords = (random.randint(0, self.x - 1), random.randint(0, self.y - 1))

            self.setCoords(coords[0], coords[1], System(self.env))
