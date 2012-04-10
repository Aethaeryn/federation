=========
TODO LIST
=========

Python
------
* db <---> game <---> json

  * Finish: Spacecraft, Component

  * Then: Game

  * Add: Structure, Unit, Body, Map (System, Sector)

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

* Map grid navigation.

  * Fix the keyboard scrolling so that diagonals, etc., work.

  * Allow mouse click+drag movement on both board and mini-map.

* Rework the GUI to use just one <canvas> if possible

* Add environment object sprites to the board.

* Fix map edge detection system.

* Add back in the mouseover information.

  * Find out which pixel-sized square the mouse is over on the board.

  * Find out which hex that square is in.

  * Find out what is located on that hex.
