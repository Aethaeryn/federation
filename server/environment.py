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

import copy, data

class EnvironmentObject(object):
    # Makes sure the dictionary can be appropriately instantiated as an object, and then does so.
    def dictionaryToInstance(self, dictionary):
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
                raise Exception('Missing entry ' + entry + ' not in data file for item ' + dictionary.name)

            elif 'name' not in dictionary:
                raise Exception('Missing name for an entry!')

        # Any optional instance variable that is missing will be set to false.
        for entry in optional:
            if entry not in dictionary:
                self.__dict__[entry] = False

        # Every entry in the dictionary, assuming no exception has been thrown, is added as an instance variable.
        self.__dict__.update(dictionary)

    # Printing an environmental object gives its name.
    def __str__(self):
        return self.name

class Component(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'size', 'cost'])
        self.optional = set(['hitpoints', 'shields', 'sensors', 'speed', 'cargo', 'dock', 'crew', 'hyperspace', 'special', 'wep_damage', 'wep_speed', 'wep_type', 'wep_special', 'unsellable'])

        # Reads in the ship data to create a component object.
        self.dictionaryToInstance(dictionary)
        self.sizeTraits()

    # Sets the size and HP based on component size.
    def sizeTraits(self):
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
        self.required = set(['name', 'description', 'size', 'base_cost', 'component_list', 'component_max'])
        self.optional = set(['special', 'inherits'])

        self.dictionaryToInstance(dictionary)

        # These are stats set elsewhere, not by the config dictionary.
        customized_stats = ['custom_name', 'hitpoints', 'shields', 'sensors', 'speed', 'cargo', 'dock', 'crew', 'hyperspace', 'damage_hitpoints', 'damage_shields', 'components_in', 'component_stat']

        for stat in customized_stats:
            self.__dict__[stat] = False

        # The value is first set to the base cost. Any component then adds to its value.
        self.value = self.base_cost

    # Uses the components in component_list to modify the spacecraft stats.
    def initializeComponents(self, components):
        self.component_stat = []

        for component in self.component_list:
            self.addComponent(components[component])

    def addComponent(self, component):
        if self.components_in + component.exp_size <= self.component_max:
            self.components_in += component.exp_size

            # Allowed stats to read.
            stats = set(['hitpoints', 'shields', 'sensors', 'speed', 'cargo', 'dock', 'crew', 'hyperspace'])

            # Adds to the spacecraft's stats with each component stat.
            for stat in dir(component):
                if stat in stats:
                    value = getattr(component, stat)

                    if value and value != 0:
                        if type(value) is int:
                            setattr(self, stat, (value + getattr(self, stat)))

                        elif type(value) is bool:
                            setattr(self, stat, True)

                # Cost is a special case because it adds to value.
                elif stat == 'cost':
                    setattr(self, 'value', (getattr(component, 'cost') + getattr(self, 'value')))

            # Keeps track of damage information for each component.
            self.component_stat.append({component.name : {"enabled": True, "damage_hitpoints": 0, "damage_shields": 0}})

        # Not enough room means it's removed from the list.
        else:
            self.component_list.remove(component.name)

    def sellComponent(self, component):
        if component in self.component_list:
            for i in range(len(component_list)):
                if component_list[i] == component:
                    self.component_list.pop(i)
                    self.component_stat.pop(i)
                    return

class Structure(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'hitpoints', 'cost'])
        self.optional = set(['special', 'shields', 'wep_damage', 'wep_speed', 'wep_type', 'wep_special'])

        self.dictionaryToInstance(dictionary)

class Unit(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description', 'hitpoints', 'cost'])
        self.optional = set(['damage', 'special'])

        self.dictionaryToInstance(dictionary)

class Body(EnvironmentObject):
    def __init__(self, dictionary):
        self.required = set(['name', 'description'])
        self.optional = set(['owner'])

        self.dictionaryToInstance(dictionary)

        # self.removed = set(['place_name', 'variant', 'effects'])

        # self.variants   = set([''])
        # self.structures = []

        # if self.variant not in self.variants:
        #    raise Exception("This isn't a valid variant for a " +
        #                    self.name + "!")

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
        self.inheritSpacecraft()
        self.objectifyDictionary()

        # Has the spacecrafts' component lists modify spacecraft stats. 
        for craft_type in self.obj["spacecraft"]:
            self.obj["spacecraft"][craft_type].initializeComponents(self.obj["component"])

    # Handles spacecraft inheritance.
    def inheritSpacecraft(self):
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
    def objectifyDictionary(self):
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

    # Increments the unique identifier of environment objects and returns a copy.
    # Use this to place a copy of an environmental object in the game environment.
    def get(self, obj_type, obj_name):
        self.obj_id += 1
        
        obj_copy = copy.copy(self.obj[obj_type][obj_name])
        obj_copy["obj_id"] = self.obj_id
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
