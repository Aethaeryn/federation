# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

from flask import Flask

app = Flask(__name__)

from federation import game, public

app.game = game.Game()
