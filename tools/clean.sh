#!/usr/bin/env bash

# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://opensource.org/licenses/MIT

# This script removes all the compiled and generated Python and JavaScript
# files, returning Federation to its original state.
#
# This file is essentially the opposite of coffee.sh

cd $( dirname "${BASH_SOURCE[0]}" )"/../federation/"; rm *.pyc
cd "static/script/"; rm *.js
cd ..; rmdir script
