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

"""Serves the public data API json and game client html using flask for
dynamic rendering of the content.
"""

from server import app
from flask import json, render_template
from os import path
import re

@app.route('/data/')
def data():
    """Tells the client which pages to look for in the data directory for
    JSON information to parse.
    """
    return json.dumps({'environment' : True})

@app.route('/data/environment')
def environment():
    """Displays the public data from server/data/environment in a way that
    the clients can parse using JSON.
    """
    return json.dumps(app.game.env.convert())

# @app.route('/data/location')
# def loc():
#     return json.dumps(app.game.system.convert())

@app.route('/')
def game():
    """Creates an html page that uses javascript with canvas to format the
    main game board. This serves as a client built into the server so that
    downloading an external client is not required.
    """
    canvases = ['header', 'board', 'sidebar', 'footer']
    html     = ''

    for canvas in canvases:
        html += '<canvas id="%s"></canvas> ' % canvas

    return render_template('basic.html', body = html, javascript = 'board.js')

@app.route('/about.html')
def about():
    """Provides an about page that explains what Federation is going to be
    to the public while Federation is still a work in progress.
    """
    infile = open(path.join(path.dirname(__file__), 'data/about.txt'))
    content = infile.read()
    infile.close()

    content = re.sub('\n\n', '\n\n  <br><br>\n\n', content)

    return render_template('basic.html', body = content)
