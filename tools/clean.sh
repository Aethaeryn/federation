#!/usr/bin/env bash

#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


# This script removes all the compiled and generated Python and JavaScript
# files, returning Federation to its original state.
#
# This file is essentially the opposite of coffee.sh

cd $( dirname "${BASH_SOURCE[0]}" )"/../server/"; rm *.pyc
cd "static/script/"; rm *.js
cd ..; rmdir script
