'''This file does all of the actions necessary to set up Federation
before running it for the first time.

Currently, this just sets up the JavaScript files by downloading the
libraries and compiling the CoffeeScript into JavaScript.

Copyright (c) 2011, 2012 Michael Babich
See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php
'''
import execjs, requests, io
from os import path, listdir, mkdir

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
        self.source   = self._get_source(filename)
        self.compiled = execjs.get().compile(self.source)

    def _get_source(self, filename):
        '''Turns the source code of a file into a string that Python
        can understand.
        '''
        source_file = io.open(filename, 'r', encoding='utf8')
        source      = source_file.read()
        source_file.close()
        return source

    def compile(self, filename):
        '''Uses the CoffeeScript compiler to compile a .coffee file
        into JavaScript.
        '''
        source = self._get_source(filename)
        return self.compiled.call('CoffeeScript.compile', source)

def write_file(destination, content):
    '''Writes a string of certain Unicode content to a given
    destination file.
    '''
    destination = io.open(destination, 'w', encoding='utf8')
    destination.write(content)
    destination.close()

def get_libraries(directory):
    '''Fetches JavaScript libraries from the Internet if they are not
    already in the JavaScript directory.
    '''
    js_lib = {'jquery.js'        : 'http://code.jquery.com/jquery-1.7.2.min.js',
              'coffee-script.js' : 'http://jashkenas.github.com/coffee-script/extras/coffee-script.js'}

    for library in js_lib:
        if library not in listdir(directory):
            downloaded  = requests.get(js_lib[library])
            destination = "%s%s" % (directory, library)
            content     = downloaded.content
            write_file(destination, content)

def compile_coffee(coffee_dir, script_dir):
    '''Turns a directory full of CoffeeScript files into a directory
    full of JavaScript files using a CoffeeScript compiler object.
    '''
    coffee = CoffeeScript(script_dir + 'coffee-script.js')

    for filename in listdir(coffee_dir):
        js_filename = '%s%s.js' % (script_dir, filename.split('.')[0])
        compiled    = coffee.compile(coffee_dir + filename)
        write_file(js_filename, compiled)

def main():
    '''Sets up various things that are required for running
    Federation.
    '''
    coffee_dir = location('src/')
    static_dir = location('federation/static/')
    script_dir = static_dir + 'script/'

    if 'script' not in listdir(static_dir):
        mkdir(script_dir)

    get_libraries(script_dir)
    compile_coffee(coffee_dir, script_dir)

if __name__ == '__main__':
    main()
