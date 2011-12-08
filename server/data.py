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

import yaml

# Handles .yml files in the data directory.
class ParseYAML():
    # Parses all of the given data into the self.parsed dictionary.
    def __init__(self, directory, filenames):
        self.parsed = {}

        for filename in filenames:
            self.parsed[filename] = self.parse(directory, filename)

    # Opens the yaml data from a given file and returns it as a Python dictionary.
    def parse(self, directory, filename):
        conf    = open('data/' + directory + '/' + filename + '.yml', 'r')
        yaml_in = yaml.load(conf)
        conf.close()

        for key in yaml_in:
            yaml_in[key]['name'] = key

        return yaml_in
