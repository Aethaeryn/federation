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

"""simple_client -- A simple Federation client.

This client simply parses URLs containing game data as a way of testing
the server-to-client API on third party clients.

This client does not handle errors very well and so is only useful for
development purposes. It breaks very easily.
"""

from sys import argv
import urllib, urllib2, cookielib
import json

def print_dictionary(data, level):
    """Recursively prints the contents of a dictionary in a format for
    human reading in terminals.
    """
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
    """Recursively prints the contents of a list in a format for human
    reading in terminals.
    """
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

def login(url):
    """Tests the login system by using a test user and password and then
    trying to access restricted JSON data.
    """
    url += 'login'

    # http://xkcd.com/936
    data = {'user' : 'michael',
            'password' : 'correcthorsebatterystaple'}

    data = urllib.urlencode(data)

    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)
    print json.loads(response.read())["success"]

def data(url):
    """Handles reading the data aspect of the Federation game server.
    """
    url += 'data/'

    response = urllib2.urlopen(url)
    data_files = json.loads(response.read())

    for data_file in data_files:
        if data_files[data_file] == True:
            new_url = url + data_file
            response = urllib2.urlopen(new_url)
            print print_dictionary(json.loads(response.read()), 0)

def use_url(url):
    """Uses the URL to test the various aspects of the API.
    """
    if url[-1] != '/':
        url += '/'

    # data(url)
    login(url)

def main():
    # You should provide a full url as its sole argument.
    if len(argv) == 2:
        use_url(argv[1])

    # Otherwise, it assumes you're connecting to a local test server.
    elif len(argv) == 1:
        parse_data("http://localhost:8080/")

    else:
        print 'You need to specify a server URL!'

main()
