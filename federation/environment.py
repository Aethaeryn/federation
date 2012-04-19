'''This turns the federation/data/environment config files into stuff
that the game can understand.

Copyright (c) 2011, 2012 Michael Babich
See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php
'''
import copy, yaml
from federation import database
from os import path

def _parse_data(directory, filenames):
    '''Takes a string (i.e. only one file) or a list of strings that
    are files in the data directory and puts them into dictionaries
    that the game can understand.
    '''
    data = path.join(path.dirname(__file__), 'data')
    ext = 'yml'

    def _open_yaml(location):
        '''Opens the yaml data from a given file and returns it in
        dictionary form, with a special case for environment. This
        special case makes a new entry called name in the dictionary
        and sets it as the name of the environmental object.
        '''
        conf    = open(location, 'r')
        yaml_in = yaml.load(conf)
        conf.close()

        if 'environment' in location:
            for key in yaml_in:
                yaml_in[key]['name'] = key

        return yaml_in

    if type(filenames) is str:
        filenames = [filenames]

    parsed = {}

    for filename in filenames:
        full_path = path.join(data, directory, '%s.%s' % (filename, ext))
        parsed[filename] = _open_yaml(full_path)

    return parsed

class Component():
    def __init__(self, dictionary):
        '''Reads in the ship data to create a component object.
        '''
        self.__dict__.update(dictionary)

        if 'hitpoints' not in dictionary:
            self.hitpoints = 0

        self.size_traits()

    def size_traits(self):
        '''Sets the size and HP based on the component size.
        '''
        if self.size == 'Small Component':
            self.hitpoints += 5
            self.exp_size   = 1

        elif self.size == 'Medium Component':
            self.hitpoints += 10
            self.exp_size   = 2

        elif self.size == 'Large Component':
            self.hitpoints += 20
            self.exp_size   = 4

class Spacecraft():
    def __init__(self, dictionary):
        '''Turns a dictionary into a Spacecraft object.
        '''
        self.__dict__.update(dictionary)

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
        '''Uses the components in component_list to modify the
        spacecraft stats.
        '''
        for component in self.component_list:
            self.add_component(components, component)

    def add_component(self, components, component_name):
        '''Adds a component's stats to the spacecraft's stats.
        '''
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
    '''When instantiated, it turns the files from data/environment
    into something that the rest of the game can understand.
    '''
    obj    = {}

    def __init__(self):
        '''Creates a dictionary of object types by parsing the data
        files for environment objects and then having the component
        lists of the spacecrafts modify their stats.
        '''
        directory = 'environment'
        filenames = ['component', 'spacecraft']

        self.obj = _parse_data(directory, filenames)
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
        '''Handles spacecraft inheritance by adding the inherited
        components to the top of the component list.
        '''
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
        '''Converts the objects into a dictionary.
        '''
        environmental_objs = {}

        for obj_type in self.obj:
            dictionary = {}

            for key in self.obj[obj_type]:
                dictionary[key] = self.obj[obj_type][key].__dict__

            environmental_objs[obj_type] = dictionary

        return environmental_objs

class Environment2():
    '''When instantiated, this reads in configuration data from the
    environment folder and then writes it to the database.
    '''
    def __init__(self):
        directory = 'environment'
        filenames = ['spacecraft', 'component', 'structure', 'unit', 'body']

        obj = _parse_data(directory, filenames)

        for filename in obj:
            for key in obj[filename]:
                if filename == 'spacecraft':
                    item = database.ModelSpacecraft(obj[filename][key])

                elif filename == 'component':
                    item = database.ModelComponent(obj[filename][key])

                elif filename == 'structure':
                    item = database.ModelStructure(obj[filename][key])

                elif filename == 'unit':
                    item = database.ModelUnit(obj[filename][key])

                elif filename == 'body':
                    item = database.ModelBody(obj[filename][key])

                database.session.add(item)

        database.session.commit()
