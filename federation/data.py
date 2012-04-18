# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

""" Handles the custom data files that come with the server. These
include the yaml files in data and the header.html template for custom
HTML code.
"""

import yaml
from os import path, listdir

class Parse():
    """ Puts the yaml files from the data directory into a form that
    the game understands.
    """

    DIR = path.join(path.dirname(__file__), 'data/')
    EXT = '.yml'

    def __init__(self, directory, filenames):
        """Takes a string (i.e. only one file) or a list of strings
        and puts it into the self.parsed dictionary.
        """

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

    @classmethod
    def parse(self, directory, filename):
        """Opens the yaml data from a given file and returns it in
        dictionary form, with a special case for environment. This
        special case makes a new entry called name in the dictionary
        and sets it as the name of the environmental object.
        """

        if directory[-1] != '/':
            directory += '/'

        conf    = open(self.DIR + directory + filename + self.EXT, 'r')
        yaml_in = yaml.load(conf)
        conf.close()

        if 'environment' in directory:
            for key in yaml_in:
                yaml_in[key]['name'] = key

        return yaml_in

def parse_header():
    """ Gets the custom HTML from templates/header.html, if it exists.
    """

    template_path = path.join(path.dirname(__file__), 'templates')
    templates     = listdir(template_path)

    if 'header.html' in templates:
        header = open(path.join(template_path, 'header.html'), 'r')
        text   = header.read()

        header.close()
        return text

    else:
        return ''
