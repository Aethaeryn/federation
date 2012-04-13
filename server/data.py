#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


import yaml
from os import path, listdir

# Handles .yml files in the server/data directory.
class Parse():
    DIR = path.join(path.dirname(__file__), 'data/')
    EXT = '.yml'

    # Parses all of the given data into the self.parsed dictionary.
    def __init__(self, directory, filenames):
        # This handles one file (a string) or a list of strings.
        if type(filenames) is str:
            filenames = [filenames]

        self.parsed = {}

        if directory[-1] != '/':
            directory += '/'

        for filename in filenames:
            try:
                self.parsed[filename] = self.parse(directory, filename)
            except:
                raise Exception('Error in parsing '
                                + self.DIR + directory + filename + self.EXT)

    # Opens the yaml data from a given file and returns it as a dictionary.
    @classmethod
    def parse(self, directory, filename):
        if directory[-1] != '/':
            directory += '/'

        conf    = open(self.DIR + directory + filename + self.EXT, 'r')
        yaml_in = yaml.load(conf)
        conf.close()

        # If we're parsing an environment object here, we'll make a new entry
        # called name and make it the name of the object.
        if 'environment' in directory:
            for key in yaml_in:
                yaml_in[key]['name'] = key

        return yaml_in

# Gets server customizations.
def parse_header():
    template_path = path.join(path.dirname(__file__), 'templates')
    templates     = listdir(template_path)

    if 'header.html' in templates:
        header = open(path.join(template_path, 'header.html'), 'r')
        text   = header.read()
        return text

    else:
        return ''
