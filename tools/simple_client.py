#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files (the
#    "Software"), to deal in the Software without restriction, including
#    without limitation the rights to use, copy, modify, merge, publish,
#    distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so, subject to
#    the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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

    data     = urllib.urlencode(data)
    request  = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    status   = json.loads(response.read())["success"]

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

    login(url)
    data(url)

def main():
    # You should provide a full url as its sole argument.
    if len(argv) == 2:
        use_url(argv[1])

    # Otherwise, it assumes you're connecting to a local test server.
    elif len(argv) == 1:
        use_url("http://localhost:8080/")

    else:
        print 'You need to specify a server URL!'

main()
