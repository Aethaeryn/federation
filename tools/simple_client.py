#    Federation
#    Copyright (C) 2011 Michael Babich
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

from sys import argv
import urllib2
import json

def parse_json(json_data):
    dictionary = json.loads(json_data)

    for key1 in dictionary:
        section = "%s:" % key1
        print section.upper()

        for key2 in dictionary[key1]:
            print "  %s:" % key2

            for key3 in dictionary[key1][key2]:
                attribute = key3 + ":"
                value     = dictionary[key1][key2][key3]

                print "    %-12s %s" % (attribute, value)

            print

        print

def parse_data(url):
    if url[-1] != '/':
        url += '/'

    if url[-5:] != 'data/':
        url += 'data/'

    #### fixme: Perhaps have data/ provide a list of available data files.
    data_files = ['environment']

    for data_file in data_files:
        data_url = url + data_file
        response = urllib2.urlopen(data_url)
        parse_json(response.read())


def main():
    if len(argv) == 2:
        parse_data(argv[1])
    else:
        print 'You need to specify a server URL!'

main()
