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

import yaml, json, os, datetime, time

# Handles .yml files in the server/data directory.
class Parse():
    DIR = 'data/'
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
                raise Exception('Error in parsing Federation/server/' + self.DIR + directory + filename + self.EXT)

    # Opens the yaml data from a given file and returns it as a Python dictionary.
    @classmethod
    def parse(self, directory, filename):
        if directory[-1] != '/':
            directory += '/'

        conf    = open(self.DIR + directory + filename + self.EXT, 'r')
        yaml_in = yaml.load(conf)
        conf.close()

        # Environmental objects are dictionaries, and they key also becomes the 'name' entry.
        if 'environment' in directory:
            for key in yaml_in:
                yaml_in[key]['name'] = key

        return yaml_in

# Writes .json files to html/data.
class Write():
    DIR = '../html/'

    def __init__(self, directory):
        # The directory must be in the public /html folder, not in /server 
        self.directory = self.DIR + directory + '/'

        # The directory might not exist at this point.
        if directory not in os.listdir(self.DIR):
            os.mkdir(self.directory)

    # Writes a .json file to be parsed by the client.
    def write(self, filename, dictionary):
        json_msg = json.dumps(dictionary, indent=4)

        out      = open(self.directory + filename + '.json', 'w')
        out.write(json_msg)
        out.close()

# Provides very limited access to datetime with static methods.
class Time():
    @classmethod
    def get(self):
        return datetime.datetime.utcnow()

    @classmethod
    def getMinutes(self, mins):
        return datetime.timedelta(minutes=mins)

    @classmethod
    def sleep(self, seconds):
        return time.sleep(seconds)
