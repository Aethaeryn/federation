#!/usr/bin/env bash

#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


# This is a quick script that takes you to the root Federation directory
# and compiles CoffeeScript to JavaScript. You need to have CoffeeScript
# installed for this to work.
#
# More sophisticated conditionals will be added when Federation is ready. 

cd $( dirname "${BASH_SOURCE[0]}" )"/.."

if [ ! -d "server/static/script" ]; then
    mkdir "server/static/script"
fi

if [ ! -f "server/static/script/jquery.js" ]; then
    curl -o server/static/script/jquery.js http://code.jquery.com/jquery-1.7.2.min.js
fi

coffee --compile --output server/static/script/ src/
