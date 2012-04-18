# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

import execjs, requests
from os import path, listdir, mkdir

def location(target):
    return path.join(path.dirname(__file__), target)

class CoffeeScript():
    def __init__(self, filename):
        self.file     = filename
        source_file   = open(self.file, 'r')
        self.source   = source_file.read()
        self.compiled = execjs.get().compile(self.source)

        source_file.close()

    def compile(self, filename):
        source_file = open(filename, 'r')
        source      = source_file.read()

        source_file.close()
        return self.compiled.call('CoffeeScript.compile', source)

def get_libraries(directory):
    js_lib = {'jquery.js'        : 'http://code.jquery.com/jquery-1.7.2.min.js',
              'coffee-script.js' : 'http://jashkenas.github.com/coffee-script/extras/coffee-script.js'}

    for library in js_lib:
        if library not in listdir(directory):
            downloaded  = requests.get(js_lib[library])
            destination = "%s%s" % (directory, library)
            destination = open(destination, 'w')
            content     = downloaded.content

            destination.write(content)
            destination.close()

def compile_coffee(coffee_dir, script_dir):
    coffee = CoffeeScript(script_dir + 'coffee-script.js')

    for filename in listdir(coffee_dir):
        js_filename = '%s%s.js' % (script_dir, filename.split('.')[0])
        destination = open(js_filename, 'w')
        compiled    = coffee.compile(coffee_dir + filename)

        destination.write(compiled)
        destination.close()

def main():
    coffee_dir = location('src/')
    static_dir = location('federation/static/')
    script_dir = static_dir + 'script/'

    if 'script' not in listdir(static_dir):
        mkdir(script_dir)

    get_libraries(script_dir)

    compile_coffee(coffee_dir, script_dir)

if __name__ == '__main__':
    main()
