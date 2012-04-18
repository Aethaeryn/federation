# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

import execjs
from os import path, listdir

def location(target):
    return path.join(path.dirname(__file__), target)

class CoffeeScript():
    def __init__(self):
        self.file     = location('coffee-script.js') #### fixme: put it in another location
        self.source   = open(self.file, 'r').read()
        self.compiled = execjs.get().compile(self.source)

    def compile(self, filename):
        source = open(filename, 'r').read()
        return self.compiled.call('CoffeeScript.compile', source)

def main():
    coffee     = CoffeeScript()
    coffee_dir = location('src/')
    compiled   = {}

    for filename in listdir(coffee_dir):
        compiled[filename] = coffee.compile(coffee_dir + filename)

    #### fixme: finish replacing tools/coffee.sh

main()
