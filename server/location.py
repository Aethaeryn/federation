#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


import random, copy

# Provides certain algorithms for hex board calculations.
# Takes in location tuples such as (0, 0)
class Location:
    # Calculates distance on a hex board.
    @classmethod
    def distance(self, start_location, end_location):
        horizontal = abs(start_location[0] - end_location[0])

        penalty = 0

        if (((start_location[0] % 2) and not (end_location[0] % 2) and start_location[1] < end_location[1])
            or (end_location[0] % 2) and not (start_location[0] % 2) and end_location[1] < start_location[1]):
            penalty = 1

        alt_distance = abs(start_location[1] - end_location[1]) + penalty + (horizontal / 2)

        return max(horizontal, alt_distance)

    # Returns a set of tuple (x, y) coordinates in the radius range.
    @classmethod
    def radius(self, location, radius):
        radius_set = set([])

        # Case 1: The radius is even.
        if not radius % 2:

            # Generates the left side of the hex range.
            for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
                radius_set.add((location[0] - radius, location[1] + i))

            # Generates the right side of the hex range
            for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
                radius_set.add((location[0] + radius, location[1] + i))

            # Connects the corners on the other sides.
            y1  = location[1] - radius
            y2  = location[1] + radius
            x1  = location[0]
            x2  = location[0]

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

# *** TODO: REWRITE TO GENERATE USING THE DB. *** #

# Holds the large environmental objects in a star system.
class System():
    def __init__(self):
        # self.size = (random.randint(60, 70), random.randint(60, 70))
        self.size = (40, 40)

        self.type_zero_system()

    # A type zero star system has a star at the center and looks like the
    # solar system. This is being used for debug purposes.
    def type_zero_system(self):
        center = ((self.size[0] - 1) / 2, (self.size[1] - 1) / 2)

        star     = ('body', 'Star')
        planet   = ('body', 'Planet')
        asteroid = ('body', 'Asteroid Field')

        self.setCoords(center[0], center[1], star)

        distances = [1, 2, 3, 4, 8, 11, 14, 17]

        # The planets start in x alignment with each other.
        for distance in distances:
            self.setCoords(center[0], center[1] + distance, planet)

        # Use radius to generate belt instead.

        # belt_distance = 6
        # self.accessCoords(center[0], center[1] + belt_distance).addBody(asteroid)
        # self.accessCoords(center[0], center[1] + belt_distance + 1).addBody(asteroid)

# Holds star systems.
class Sector(Map):
    # Creates a star sector with an environment.py instance, and a max x and y.
    def __init__(self, x, y):
        Map.__init__(self, x, y)

        # self.generate_sector()

        self.setCoords(0, 0, System())

        self.name = 'Sector'

    # Places stars randomly in the map.
    def generate_sector(self):
        for i in range(self.x * self.y / 5):
            coords = (random.randint(0, self.x - 1),
                      random.randint(0, self.y - 1))

            self.setCoords(coords[0], coords[1], System())
