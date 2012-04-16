#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


import copy
from federation import data, database

class EnvironmentObject(object):
    """An environment object is something that exists as a physical
    object in the game world and on the game board, as read in from
    the YAML data files.
    """
    def __init__(self, dictionary):
        """Makes sure that the dictionary can be appropriately
        instantiated as an object, and then does so.
        """
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

class Component(EnvironmentObject):
    def __init__(self, dictionary):
        """Reads in the ship data to create a component object.
        """
        self.required = set(['name', 'description', 'size', 'cost'])
        self.optional = set(['hitpoints', 'shields', 'sensors', 'speed',
                             'cargo', 'dock', 'crew', 'hyperspace', 'special',
                             'wep_damage', 'wep_speed', 'wep_type',
                             'wep_special', 'unsellable'])

        super(Component, self).__init__(dictionary)
        self.size_traits()

    def size_traits(self):
        """Sets the size and HP based on the component size.
        """
        if self.size == 'Small Component':
            self.hitpoints += 5
            self.exp_size   = 1

        elif self.size == 'Medium Component':
            self.hitpoints += 10
            self.exp_size   = 2

        elif self.size == 'Large Component':
            self.hitpoints += 20
            self.exp_size   = 4

class Spacecraft(EnvironmentObject):
    def __init__(self, dictionary):
        """Turns a dictionary into a Spacecraft object.
        """
        # These stats are read in from outside.
        self.required = set(['name', 'description', 'size', 'base_cost',
                             'component_list', 'component_max'])
        self.optional = set(['special', 'inherits'])

        super(Spacecraft, self).__init__(dictionary)

        # These are stats set elsewhere, not by the config dictionary.
        customized_stats = ['hitpoints', 'shields', 'sensors',
                            'speed', 'cargo', 'dock', 'crew', 'hyperspace',
                            'components_in']

        for stat in customized_stats:
            self.__dict__[stat] = False

        # The value is first set to the base cost.
        # Any component should add to its value.
        self.value = self.base_cost

    def initialize_components(self, components):
        """Uses the components in component_list to modify the
        spacecraft stats.
        """
        for component in self.component_list:
            self.add_component(components, component)

    def add_component(self, components, component_name):
        """Adds a component's stats to the spacecraft's stats.
        """
        component = components[component_name]

        if self.components_in + component.exp_size >= self.component_max:
            self.component_list.remove(component.name)
            raise Exception('Not enough room for component ' + component.name)

        self.components_in += component.exp_size
        self.value         += component.cost

        stats = set(['hitpoints', 'shields', 'sensors', 'speed', 'cargo',
                     'dock', 'crew', 'hyperspace'])

        for stat in dir(component):
            if stat in stats:
                value = component.__dict__[stat]

                if type(value) is int:
                    self.__dict__[stat] += value

                if value and type(value) is bool:
                    self.__dict__[stat] = True

class Environment():
    """When instantiated, it turns the files from data/environment
    into something that the rest of the game can understand.
    """
    obj    = {}

    def __init__(self):
        """Creates a dictionary of object types by parsing the data
        files for environment objects and then having the component
        lists of the spacecrafts modify their stats.
        """
        directory = 'environment'
        filenames = ['component', 'spacecraft']

        parse    = data.Parse(directory, filenames)
        self.obj = parse.parsed
        self.inherit_spacecraft()

        for filename in self.obj:
            for key in self.obj[filename]:
                in_data = self.obj[filename].pop(key)

                if filename == 'component':
                    self.obj[filename][key] = Component(in_data)

                elif filename == 'spacecraft':
                    self.obj[filename][key] = Spacecraft(in_data)

        for craft_type in self.obj['spacecraft']:
            self.obj['spacecraft'][craft_type].initialize_components(self.obj['component'])

    def inherit_spacecraft(self):
        """Handles spacecraft inheritance by adding the inherited
        components to the top of the component list.
        """
        for spacecraft in self.obj['spacecraft']:
            if 'inherits' in self.obj['spacecraft'][spacecraft]:
                old_data = self.obj['spacecraft'][spacecraft]

                inherits = old_data['inherits']

                new_list = copy.copy(self.obj['spacecraft'][inherits]['component_list'])

                for component in self.obj['spacecraft'][spacecraft]['component_list']:
                    new_list.append(component)

                old_data['component_list'] = new_list

                self.obj['spacecraft'][spacecraft] = copy.copy(self.obj['spacecraft'][inherits])
                self.obj['spacecraft'][spacecraft].update(old_data)

    def convert(self):
        """Converts the objects into a dictionary.
        """
        environmental_objs = {}

        for obj_type in self.obj:
            dictionary = {}

            for key in self.obj[obj_type]:
                dictionary[key] = self.obj[obj_type][key].__dict__

            environmental_objs[obj_type] = dictionary

        return environmental_objs

class Environment2():
    def __init__(self):
        directory = 'environment'
        filenames = ['structure', 'unit', 'body']

        obj = data.Parse(directory, filenames).parsed

        for filename in obj:
            for key in obj[filename]:
                if filename == 'structure':
                    structure = database.ModelStructure(obj[filename][key])

                    database.session.add(structure)

                elif filename == 'unit':
                    unit = database.ModelUnit(obj[filename][key])

                    database.session.add(unit)

                elif filename == 'body':
                    body = database.ModelBody(obj[filename][key])

                    database.session.add(body)

        database.session.commit()
