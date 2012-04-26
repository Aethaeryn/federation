# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This turns the federation/data/environment config files into stuff
that the game can understand.
'''
import yaml
from federation.database import model, database, session
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

def environment():
    '''This reads in configuration data from the environment folder
    and then writes it to the database.
    '''
    directory = 'environment'
    filenames = ['spacecraft', 'component', 'structure', 'unit', 'body']

    obj = _parse_data(directory, filenames)

    for filename in obj:
        for key in obj[filename]:
            if filename == 'spacecraft':
                item = model.ModelSpacecraft(obj[filename][key])

            elif filename == 'component':
                item = model.ModelComponent(obj[filename][key])

            elif filename == 'structure':
                item = model.ModelStructure(obj[filename][key])

            elif filename == 'unit':
                item = model.ModelUnit(obj[filename][key])

            elif filename == 'body':
                item = model.ModelBody(obj[filename][key])

            session.add(item)

    session.commit()
