=========
TODO LIST
=========

Python
------
* db <---> json

  * Make every database element seemlessly transition to JSON that can be
    accessed, including a link to its environment information that's read
    into JSON already.

* Game elements.

  * Map generation.

  * Territories and bodies.

    * Ownership and stats.

    * clean up location.py

    * Hex grid calculation algorithms.

* Game code.

  * Turns.

    * Implement turns.

    * Implement things that change on turn switch.

  * Movement.

  * Combat.

* Eventually: Authentication.


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
