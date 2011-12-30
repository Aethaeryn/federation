#    Federation
#    Copyright (C) 2011 Michael Babich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def game():
    infile  = open('client/game.html')
    content = infile.read()
    infile.close()
    return content

@app.route('/board.js')
def board():
    infile = open('client/board.js')
    conent = infile.read()
    infile.close()
    return conent

if __name__ == "__main__":
    os.chdir("..")
    app.run()

else:
    # Makes the directory relative to the main Federation folder before running.
    federation_root = __file__[:-(len("/server/app.py"))]
    os.chdir(federation_root)
