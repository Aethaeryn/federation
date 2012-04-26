# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''Provides certain algorithms for hex board calculations.
'''
def distance(start_location, end_location):
    '''Calculates the difference between two points on a hex board
    expressed in (x, y) coordinates.
    '''
    horizontal = abs(start_location[0] - end_location[0])

    penalty = 0

    if (((start_location[0] % 2) and not (end_location[0] % 2) and start_location[1] < end_location[1])
        or (end_location[0] % 2) and not (start_location[0] % 2) and end_location[1] < start_location[1]):
        penalty = 1

    alt_distance = abs(start_location[1] - end_location[1]) + penalty + (horizontal / 2)

    return max(horizontal, alt_distance)

def get_radius(location, radius):
    '''Returns a set of tuple (x, y) coordinates in the radius range.
    '''
    radius_set = set([])

    # Case 1: The radius is even.
    if not radius % 2:

        # Generates the left side of the hex range.
        for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
            radius_set.add((location[0] - radius, location[1] + i))

        # Generates the right side of the hex range
        for i in range(-radius + (radius / 2), radius - (radius / 2) + 1):
            radius_set.add((location[0] + radius, location[1] + i))

        x = []
        y = []

        # Connects the corners on the other sides.
        y[0] = location[1] - radius
        y[1] = location[1] + radius
        x[0] = location[0]
        x[1] = location[0]

        for i in range(radius):
            radius_set.add((x[0], y[0]))
            radius_set.add((x[1], y[0]))
            radius_set.add((x[0], y[1]))
            radius_set.add((x[1], y[1]))

            # Odds walk the hexes a certain way.
            if x[0] % 2:
                x[0] -= 1
                x[1] += 1
                y[1] -= 1

            # Evens walk the hexes another way.
            else:
                x[0] -= 1
                x[1] += 1
                y[0] += 1

    return radius_set
