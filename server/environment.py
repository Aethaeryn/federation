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

import core, data
import copy

class EnvironmentObject(core.CoreObject):
    name   = ''

    # If there is a matching attribute, the key
    def dictionaryToInstance(self, dictionary):
        for key in dictionary:
            if hasattr(self, key):
                setattr(self, key, dictionary[key])

    def __str__(self):
        return self.name

class Component(EnvironmentObject):
    def __init__(self, dictionary):
        # Stores basic stats.
        self.name        = ''
        self.description = ''
        self.sellable    = True
        self.size        = ''
        self.cost        = 0
        self.hitpoints   = 0
        self.shields     = 0
        self.sensors     = 0
        self.speed       = 0

        # Stores special information.
        self.cargo       = 0
        self.dock        = 0
        self.crew        = 0
        self.hyperspace  = False
        self.special     = False

        # Stores weapon information.
        self.wep_damage  = 0
        self.wep_speed   = 0
        self.wep_type    = False
        self.wep_special = False

        # Reads in the ship data.
        self.dictionaryToInstance(dictionary)

        # Sets the size and HP based on component size.
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
        # Stores basic stats.
        self.name        = ''
        self.custom_name = False
        self.description = False
        self.size        = False
        self.base_cost   = 0
        self.hitpoints   = 0
        self.shields     = 0
        self.sensors     = 0
        self.speed       = 0

        # Stores special information.
        self.cargo       = False
        self.dock        = False
        self.crew        = False
        self.hyperspace  = False
        self.is_shipyard = False

        # Stores damage information.
        self.damage_hitpoints = 0
        self.damage_shields   = 0

        # Stores component information.
        self.component_max  = 0
        self.components_in  = 0
        self.component_list = []
        self.component_stat = []

        # Reads in the ship data.
        self.dictionaryToInstance(dictionary)

        # The value is set to the base cost, and then any component adds to its value.
        self.value = self.base_cost

    # Uses the components in component_list to modify the spacecraft stats.
    def initializeComponents(self, components):
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
                    component_list.pop(i)
                    component_stat.pop(i)
                    return

class Structure(EnvironmentObject):
    def __init__(self, dictionary):
        self.name        = ''
        self.description = ''
        self.cost        = 0
        self.hitpoints   = 0
        self.special     = False

        self.shields     = 0
        self.wep_damage  = 0
        self.wep_speed   = 0
        self.wep_type    = False
        self.wep_special = False

        self.dictionaryToInstance(dictionary)

class Unit(EnvironmentObject):
    def __init__(self, dictionary):
        self.name        = ''
        self.description = ''
        self.cost        = 0
        self.hitpoints   = 0
        self.damage      = 0
        self.veteran     = 0
        self.special     = False

        self.dictionaryToInstance(dictionary)

class Body(EnvironmentObject):
    def __init__(self, dictionary):
        self.name        = ''
        self.place_name  = ''
        self.description = ''
        self.owner       = 'Neutral'
        self.variant     = ''
        self.effects     = None

        # self.variants   = set([''])
        self.structures = []

        self.dictionaryToInstance(dictionary)

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

        # Parses the yaml data files for environment objects.
        parse    = data.ParseYAML(directory, filenames)
        self.obj = parse.parsed

        # Turns the yaml dictionaries into Python objects.
        for filename in self.obj:
            for key in self.obj[filename]:
                yaml = self.obj[filename].pop(key)

                if filename == "component":
                    self.obj[filename][key] = Component(yaml)

                elif filename == "spacecraft":
                    self.obj[filename][key] = Spacecraft(yaml)

                elif filename == "structure":
                    self.obj[filename][key] = Structure(yaml)

                elif filename == "unit":
                    self.obj[filename][key] = Unit(yaml)

                elif filename == "body":
                    self.obj[filename][key] = Body(yaml)

        # Has the spacecrafts' component lists modify spacecraft stats. 
        for craft_type in self.obj["spacecraft"]:
            self.obj["spacecraft"][craft_type].initializeComponents(self.obj["component"])

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
                dictionary[key] = self.obj[obj_type][key].getStatus()

            environmental_objs[obj_type] = dictionary

        return environmental_objs
