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


import yaml
from os import path, listdir

# Handles .yml files in the server/data directory.
class Parse():
    DIR = path.join(path.dirname(__file__), "data/")
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
