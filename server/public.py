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

import re

from server import app

from flask import json, render_template

@app.route('/data/environment')
def environment():
    return json.dumps(app.game.env.convert())

# @app.route('/data/location')
# def loc():
#     return json.dumps(app.game.system.convert())

# Eventually this will be toggleable, which means that you can force the users to use clients other than the browser-based client the web server provides.
class Client():
    @app.route('/')
    def game():
        return render_template('basic.html',
                               body       = '<canvas id="header"></canvas> <canvas id="board"></canvas> <canvas id="sidebar"></canvas> <canvas id="footer"></canvas>',
                               javascript = 'board.js')

    @app.route('/about.html')
    def about():
        infile = open('client/about.txt')
        content = infile.read()
        infile.close()

        content = re.sub('\n\n', '\n\n  <br><br>\n\n', content)

        return render_template('basic.html', body = content)

    @app.route('/board.js')
    def board():
        infile = open('client/board.js')
        content = infile.read()
        infile.close()
        return content
