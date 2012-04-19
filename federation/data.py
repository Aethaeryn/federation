'''Handles the custom data files that come with the server. These
include the yaml files in data and the header.html template for custom
HTML code.

Copyright (c) 2011, 2012 Michael Babich
See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php
'''
import yaml
from os import path

def parse(directory, filenames):
    '''Takes a string (i.e. only one file) or a list of strings that
    are files in the data directory and puts them into dictionaries
    that the game can understand.
    '''
    DIR = path.join(path.dirname(__file__), 'data')
    EXT = 'yml'

    if type(filenames) is str:
        filenames = [filenames]

    parsed = {}

    for filename in filenames:
        full_path = path.join(DIR, directory, '%s.%s' % (filename, EXT))
        parsed[filename] = _open_yaml(full_path)

    return parsed

def _open_yaml(location):
    '''Opens the yaml data from a given file and returns it in
    dictionary form, with a special case for environment. This special
    case makes a new entry called name in the dictionary and sets it
    as the name of the environmental object.
    '''
    conf    = open(location, 'r')
    yaml_in = yaml.load(conf)
    conf.close()

    if 'environment' in location:
        for key in yaml_in:
            yaml_in[key]['name'] = key

    return yaml_in
