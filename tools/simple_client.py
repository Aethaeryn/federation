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

def print_dictionary(data, level):
    spacing = "  " * level
    section = ""

    for key in data:
        section += "%s%-15s: " % (spacing, key)

        if type(data[key]) == dict:
            section += "\n" + print_dictionary(data[key], level + 1)

        elif type(data[key]) == list:
            section += "\n" + print_list(data[key], level + 1)

        else:
            section += str(data[key]) + "\n"

    return section

def print_list(data, level):
    spacing = "  " * level
    section = ""

    for item in data:
        if type(item) == dict:
            section += print_dictionary(item, level + 1) + "\n"

        elif type(item) == list:
            section += spacing + "- " + print_list(item, level + 1) + "\n"

        else:
            section += spacing + "- " + str(item) + "\n"

    return section

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
        print print_dictionary(json.loads(response.read()), 0)

def main():
    if len(argv) == 2:
        parse_data(argv[1])
    else:
        print 'You need to specify a server URL!'

main()
