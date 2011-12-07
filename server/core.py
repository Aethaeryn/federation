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

class CoreObject(object):
    def getStatus(self):
        status = {}

        for stat in dir(self):
            value = getattr(self, stat)
            types = set([str, int, bool, list, dict])

            # Iterates over all meaningful instance variables that store something.
            if (type(value) in types) and stat is not '__module__':
                status[stat] = getattr(self, stat)

        return status

    def __str__(self):
        return self.name
