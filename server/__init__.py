#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


from flask import Flask

app = Flask(__name__)

from server import game, public

app.game = game.Game(1)
