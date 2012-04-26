# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

'''This file does all of the actions necessary to set up Federation
before running it for the first time.

Currently, this just sets up the JavaScript files by downloading the
libraries and compiling the CoffeeScript into JavaScript.

This file needs an external configuration file to run.
'''
from os import path, listdir, mkdir
import execjs
import io
import requests
import yaml

CONF_FILE = 'federation/data/setup.yml'

def location(target):
    '''Turns a string that is a relative directory location into a
    full path that Python can understand.
    '''
    return path.join(path.dirname(__file__), target)

class CoffeeScript():
    '''Acts as a compiler of CoffeeScript into JavaScript if first
    provided the location of a CoffeeScript compiler that is written
    in JavaScript.
    '''
    def __init__(self, filename):
        '''Reads in the CoffeeScript compiler into a JavaScript
        environment via execjs.
        '''
        self.source   = read_file(filename)
        self.compiled = execjs.get().compile(self.source)

    def compile(self, filename):
        '''Uses the CoffeeScript compiler to compile a .coffee file
        into JavaScript.
        '''
        source = read_file(filename)
        return self.compiled.call('CoffeeScript.compile', source)

def read_file(filename):
    '''Turns a file into a string that Python can understand.
    '''
    source_file = io.open(filename, 'r', encoding='utf8')
    source      = source_file.read()
    source_file.close()
    return source

def write_file(destination, content):
    '''Writes a string of certain Unicode content to a given
    destination file.
    '''
    destination = io.open(destination, 'w', encoding='utf8')
    destination.write(unicode(content))
    destination.close()

def get_libraries(directory, libraries):
    '''Fetches JavaScript libraries from the Internet if they are not
    already in the JavaScript directory.
    '''
    for library in libraries:
        if library not in listdir(directory):
            downloaded  = requests.get(libraries[library])
            destination = path.join(directory, library)
            content     = downloaded.content
            write_file(destination, content)

def compile_coffee(coffee_dir, script_dir):
    '''Turns a directory full of CoffeeScript files into a directory
    full of JavaScript files using a CoffeeScript compiler object.
    '''
    coffee = CoffeeScript(path.join(script_dir, 'coffee-script.js'))

    for filename in listdir(coffee_dir):
        js_filename = path.join(script_dir, "%s.js" % filename.split('.')[0])
        compiled    = coffee.compile(coffee_dir + filename)
        write_file(js_filename, compiled)

def main():
    '''Sets up various things that are required for running
    Federation.
    '''
    config     = yaml.load(read_file(location(CONF_FILE)))
    coffee_dir = location(config['Directories']['Coffee'])
    static_dir = location(config['Directories']['Static'])
    script_dir = location(config['Directories']['Script'])

    if 'script' not in listdir(static_dir):
        mkdir(script_dir)

    get_libraries(script_dir, config['Libraries'])
    compile_coffee(coffee_dir, script_dir)

if __name__ == '__main__':
    main()
