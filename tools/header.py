#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#### TODO: Add the ability to change a file's headers, not just append them.

import sys

class Header():
    agpl = '''#    Federation
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

'''

    gpl = '''#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

    licenses = set(['gpl', 'agpl'])

    @classmethod
    def stamp(self, header, filename):
        # Examines the extension.
        extension = filename.split('.')[1]

        # Javascript uses '//' instead of '#' and the rest are '#'
        if extension == 'js':
            self.__dict__[header] = self.__dict__[header].replace('#', '//')

        # Reads in the old file.
        infile = open(filename, 'r')

        new_file = self.__dict__[header] + infile.read()

        infile.close()

        # Writes out the file, which now has a header.
        outfile = open(filename, 'w')

        outfile.write(new_file)

        outfile.close()

def main():
    # Checks for the right argument count.
    if len(sys.argv) != 3:
        print 'Error: The syntax is "python header.py <license> <file>"'

    # Checks for the right license.
    elif sys.argv[1] not in Header.licenses:
        print 'Error: Valid licenses are:',

        for license_name in Header.licenses:
            print license_name,

    # Tries to stamp the file.
    else:
        try:
            Header.stamp(sys.argv[1], sys.argv[2])

        except Exception:
            print 'Error with stamping file "' + sys.argv[2] + '"'

main()
