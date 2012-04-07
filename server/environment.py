#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files (the
#    "Software"), to deal in the Software without restriction, including
#    without limitation the rights to use, copy, modify, merge, publish,
#    distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so, subject to
#    the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import copy
from server import data

# An environment object is something that exists as a physical object in the
# game world and on the game board.
class EnvironmentObject(object):
    # Makes sure the dictionary can be appropriately instantiated as an object,
    # and then does so.
    def __init__(self, dictionary):
        # Popping the required and optional so they're not checked against below.
        required = self.__dict__.pop('required')
        optional = self.__dict__.pop('optional')

        # Every new instance variable must be expected by the object.
        for key in dictionary:
            if key not in required and key not in optional:
                raise Exception('Illegal value in the data file!')

        # Every new required instance variable must be provided.
        for entry in required:
            if entry not in dictionary and 'name' in dictionary:
                raise Exception('Missing entry ' + entry +
                                ' not in data file for item ' + dictionary.name)

            elif 'name' not in dictionary:
                raise Exception('Missing name for an entry!')

        # Any optional instance variable that is missing will be set to false.
        for entry in optional:
            if entry not in dictionary:
                self.__dict__[entry] = False

        # Every entry in the dictionary, assuming no exception has been thrown,
        # is added as an instance variable.
        self.__dict__.update(dictionary)

    # Printing an environmental object gives its name.
    def __str__(self):
        return self.name

class Component(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'size', 'cost'])
        self.optional = set(['hitpoints', 'shields', 'sensors', 'speed',
                             'cargo', 'dock', 'crew', 'hyperspace', 'special',
                             'wep_damage', 'wep_speed', 'wep_type',
                             'wep_special', 'unsellable'])

        # Reads in the ship data to create a component object.
        super(Component, self).__init__(dictionary)
        self.size_traits()

    # Sets the size and HP based on component size.
    def size_traits(self):
        if self.size == "Small Component":
            self.hitpoints += 5
            self.exp_size   = 1

        elif self.size == "Medium Component":
            self.hitpoints += 10
            self.exp_size   = 2

        elif self.size == "Large Component":
            self.hitpoints += 20
            self.exp_size   = 4

class Spacecraft(EnvironmentObject):
    def __init__(self, dictionary):
        # These stats are read in from outside.
        self.required = set(['name', 'description', 'size', 'base_cost',
                             'component_list', 'component_max'])
        self.optional = set(['special', 'inherits'])

        super(Spacecraft, self).__init__(dictionary)

        # These are stats set elsewhere, not by the config dictionary.
        customized_stats = ['custom_name', 'hitpoints', 'shields', 'sensors',
                            'speed', 'cargo', 'dock', 'crew', 'hyperspace',
                            'damage_hitpoints', 'damage_shields',
                            'components_in', 'component_stat']

        for stat in customized_stats:
            self.__dict__[stat] = False

        # The value is first set to the base cost.
        # Any component should add to its value.
        self.value = self.base_cost

    # Uses the components in component_list to modify the spacecraft stats.
    def initialize_components(self, components):
        self.component_stat = []

        for component in self.component_list:
            self.add_component(components, component)

    # Checks to make sure a component position is valid before acting.
    def check_position(self, position):
        if position >= len(component_list) or position < 0:
            raise Exception("Invalid component list position.")

    def enable_component(self, component, position):
        # Allowed stats to read.
        stats = set(['hitpoints', 'shields', 'sensors', 'speed', 'cargo',
                     'dock', 'crew', 'hyperspace'])

        for stat in dir(component):
            if stat in stats:
                value = component.__dict__[stat]

                if type(value) is int:
                    self.__dict__[stat] += value

                if value and type(value) is bool:
                    self.__dict__[stat] = True

        self.component_stat[position]["enabled"] = True

    def disable_component(self, component, position, change_status):
        # Allowed stats to read.
        stats = set(['hitpoints', 'shields', 'sensors', 'speed', 'cargo',
                     'dock', 'crew', 'hyperspace'])

        for stat in dir(component):
            if stat in stats:
                value = component.__dict__[stat]

                if type(value) is int:
                    self.__dict__[stat] -= value

                #### fixme: What if there's more than one component that enables this stat?
                if value and type(value) is bool:
                    self.__dict__[stat] = False

        if change_status:
            self.component_stat[position]["enabled"] = False

    def add_component(self, components, component_name):
        component = components[component_name]

        if self.components_in + component.exp_size >= self.component_max:
            self.component_list.remove(component.name)
            raise Exception("Not enough room for component " + component.name)

        self.components_in += component.exp_size
        self.value         += component.cost

        # Keeps track of damage information for each component.
        self.component_stat.append({"damage_hitpoints": 0})

        self.enable_component(component, len(self.component_stat) - 1)

    def del_component(self, components, position):
        self.check_position(position)

        component = components[self.component_list.pop(position)]
        comp_stat = self.component_stat.pop(position)

        self.components_in -= component.exp_size
        self.value         -= component.cost

        # Reverses the damage if it exists, since the spacecraft total HP is
        # going to go down.
        self.damage_hitpoints -= self.component_stat["damage_hitpoints"]

        if self.component_stat["enabled"]:
            self.disable_component(component, position, False)

    def change_component_hitpoints(self, components, position, hp_change):
        self.check_position(position)

        component = components[self.component_list[position]]
        comp_stat = self.component_stat[position]

        # Reducing the damage on an entirely damaged component will enable it.
        if comp_stat["damage_hitpoints"] == component.hitpoints and hp_change < 0:
            self.enable_component(component, position)

        comp_stat["damage_hitpoints"] += hp_change

        # Maxing out the damage on a component will diable it.
        if comp_stat["damage_hitpoints"] >= component.hitpoints:
            self.comp_stat["damage_hitpoints"] = component.hitpoints

            self.disable_component(component, position, True)

class Structure(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'hitpoints', 'cost'])
        self.optional = set(['special', 'shields', 'wep_damage', 'wep_speed',
                             'wep_type', 'wep_special'])

        super(Structure, self).__init__(dictionary)

class Unit(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'hitpoints', 'cost'])
        self.optional = set(['damage', 'special'])

        super(Unit, self).__init__(dictionary)

class Body(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description'])
        self.optional = set(['variants'])

        super(Body, self).__init__(dictionary)

        # These are stats set elsewhere, not by the config dictionary.
        customized_stats = ['custom_name', 'variant', 'owner', 'structures']

        for stat in customized_stats:
            self.__dict__[stat] = False

# The interface for environment.py. Instantiate to use this file elsewhere.
class Environment():
    obj_id = 0
    obj    = {}

    # Creates a database of object types.
    def __init__(self):
        directory = "environment"
        filenames = ["component", "spacecraft", "structure", "unit", "body"]

        # Parses the data files for environment objects.
        parse    = data.Parse(directory, filenames)
        self.obj = parse.parsed
        self.inherit_spacecraft()
        self.objectify_dictionary()

        # Has the spacecrafts' component lists modify spacecraft stats.
        for craft_type in self.obj["spacecraft"]:
            self.obj["spacecraft"][craft_type].initialize_components(self.obj["component"])

    # Handles spacecraft inheritance.
    def inherit_spacecraft(self):
        for spacecraft in self.obj['spacecraft']:
            if 'inherits' in self.obj['spacecraft'][spacecraft]:
                old_data = self.obj['spacecraft'][spacecraft]

                inherits = old_data['inherits']

                # The inherited components go at the top of the component list.
                new_list = copy.copy(self.obj['spacecraft'][inherits]['component_list'])

                for component in self.obj['spacecraft'][spacecraft]['component_list']:
                    new_list.append(component)

                old_data['component_list'] = new_list

                # Merging the inherited spacecraft with the additions.
                self.obj['spacecraft'][spacecraft] = copy.copy(self.obj['spacecraft'][inherits])
                self.obj['spacecraft'][spacecraft].update(old_data)

    # Turns the parsed dictionaries into Python objects.
    def objectify_dictionary(self):
        for filename in self.obj:
            for key in self.obj[filename]:
                in_data = self.obj[filename].pop(key)

                if filename == "component":
                    self.obj[filename][key] = Component(in_data)

                elif filename == "spacecraft":
                    self.obj[filename][key] = Spacecraft(in_data)

                elif filename == "structure":
                    self.obj[filename][key] = Structure(in_data)

                elif filename == "unit":
                    self.obj[filename][key] = Unit(in_data)

                elif filename == "body":
                    self.obj[filename][key] = Body(in_data)

    # Increments the unique identifier of environment objects and returns a
    # copy of that object.Use this to place a copy of an environmental object
    # in the game environment.
    def get(self, obj_type, obj_name):
        self.obj_id += 1

        obj_copy = copy.copy(self.obj[obj_type][obj_name])
        obj_copy.__dict__["obj_id"] = self.obj_id
        return obj_copy

    # Converts objects into a dictionary for parsing elsewhere.
    def convert(self):
        environmental_objs = {}

        for obj_type in self.obj:
            dictionary = {}

            for key in self.obj[obj_type]:
                dictionary[key] = self.obj[obj_type][key].__dict__

            environmental_objs[obj_type] = dictionary

        return environmental_objs
