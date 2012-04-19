=========
TODO LIST
=========

These are all of the items needed before Federation moves onto the
next phase of development. This is *not* an exhaustive list of all
features before Federation enters alpha, but rather a list of what to
focus on *now*.

Python
------
* db <---> json

  * Make every database element seemlessly transition to JSON that can
    be accessed.

  * Finish moving Spacecraft and Component models from environment to
    database and make sure that the data/environment JSON is just as
    functional as it was before the rewrite.

  * Sort the methods, classes, functions, variables, etc., in a
    logical manner.

  * Break up database.py and perhaps public.py into subfiles.

* Game elements.

  * Map generation.

  * Hex grid (distance/radius) calculation algorithms.

* Game code.

  * Make a new Python file that when called by a cron script
    increments the turns on a regular (e.g. every midnight) basis.

  * Movement and location.

  * Combat.

* Add in checks to database.py to make sure that the data is valid and
  that all of the required fields are provided.

  * Add reasonable defaults?

CoffeeScript
------------
* Rewrite board.js in CoffeeScript.

  * Rework the GUI to use just one <canvas> if possible

  * Fix map edge detection system.

  * Add environment sprites to the board.

* actions.coffee

  * Fix the keyboard scrolling so that diagonals, etc., work.

  * Allow mouse click+drag movement on both board and mini-map.


* Add back in the mouseover information.

  * Find out which pixel-sized square the mouse is over on the board.

  * Find out which hex that square is in.

  * Find out what is located on that hex.
