#!/usr/bin/env bash

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
