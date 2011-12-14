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

import yaml, json, os, datetime, time

# Handles .yml files in the server/data directory.
class Parse():
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

# Writes .json and .yml files to html/data.
# YAML is preferred, where available, but json is more widely supported.
class Write():
    def __init__(self, directory):
        # The directory must be in the public /html folder, not in /server 
        self.directory = '../html/' + directory + '/'

        # The directory might not exist at this point.
        if directory not in os.listdir('../html/'):
            os.mkdir(self.directory)

    # Writes a .json and a .yml file containing identical information.
    # Either file can be fetched by the client to be parsed.
    def write(self, filename, dictionary):
        json_msg = json.dumps(dictionary, indent=4)
        yaml_msg = '# This file is machine generated. Do not edit by hand.\n\n' + yaml.dump(dictionary, default_flow_style=False)

        out      = open(self.directory + filename + '.json', 'w')
        out.write(json_msg)
        out.close()

        out       = open(self.directory + filename + '.yml', 'w')
        out.write(yaml_msg)
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
