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

* Game elements.

  * Map generation.

  * Hex grid (distance/radius) calculation algorithms.

* Game code.

  * Make a new Python file that when invoked by a cron script increments
    the turns on a regular (e.g. every midnight) basis.

  * Movement and location.

  * Combat.

* Add in checks to database.py to make sure that the data is valid and
  that all of the required fields are provided.

CoffeeScript
------------
* Rewrite board.js in CoffeeScript.

  * Rework the GUI to use just one <canvas> if possible

  * Fix map edge detection system.

* actions.coffee

  * Fix the keyboard scrolling so that diagonals, etc., work.

  * Allow mouse click+drag movement on both board and mini-map.

* Add environment object sprites to the board.

* Add back in the mouseover information.

  * Find out which pixel-sized square the mouse is over on the board.

  * Find out which hex that square is in.

  * Find out what is located on that hex.
