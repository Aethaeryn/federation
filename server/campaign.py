#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
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

from server import data

class Mission():
    def __init__(self, name, directory = 'missions/'):
        if directory[-1] != '/':
            directory += '/'

        parse        = data.Parse(directory, name)
        self.mission = parse.parsed

        print self.mission

class Campaign():
    def __init__(self, name, directory='campaigns/'):
        if directory[-1] != '/':
            directory += '/'

        location      = directory + name
        filename      = 'main'
        parse         = data.Parse(location, filename)
        self.campaign = parse.parsed

        missions = self.campaign[filename]['Missions']

        for mission in missions:
            mission_data = Mission(mission, directory = location + '/missions')

def main():
    campaign = Campaign('test')
    mission = Mission('jumpgate')

main()
