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

import yaml, datetime, time

# Handles .yml files in the server/data directory.
class Parse():
    DIR = 'server/data/'
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
                raise Exception('Error in parsing Federation/server/'
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

# Provides very limited access to datetime with static methods.
class Time():
    @classmethod
    def set_next_turn_end(self, turns_per_day):
        now = datetime.datetime.utcnow()

        hour_length = 24 / turns_per_day

        # If once a day, simply escalate the days.
        if turns_per_day == 1:
            return datetime.datetime(now.year, now.month, now.day + 1)

        # If the last hour set has passed, the next turn is at midnight.
        elif (turns_per_day > 1) and (now.hour >= (hour_length * turns_per_day - 1)):
            return datetime.datetime(now.year, now.month, now.day + 1)

        # Otherwise, escalate the day's subdivision.
        else:
            return datetime.datetime(now.year, now.month, now.day,
                                     hour_length * (now.hour / hour_length) + 1)

    @classmethod
    def get(self):
        return datetime.datetime.utcnow()

    @classmethod
    def get_minutes(self, mins):
        return datetime.timedelta(minutes=mins)

    @classmethod
    def sleep(self, seconds):
        return time.sleep(seconds)
