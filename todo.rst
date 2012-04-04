=========
TODO LIST
=========

Python
------
* Database code.

  * Items not yet in the db:

    * Structure

    * Unit

    * Body

    * System

    * Sector

  * Make the translation between the three forms painless.

    * db <---> game <---> json

* Authentication and registration needs to be added.

  * Extend player code in db to store passwords safely.

* Location code.

  * Map generation.

  * Hex calculation algorithms.

* Environment code.

  * Territories and bodies.

  * Individual "instances" of spacecraft.

* Game code.

  * Turns.

  * Movement.

  * Combat.


JavaScript
----------
* Map grid navigation.

  * Fix keyboard scrolling.

  * Arrow key, WASD, and HJKL need to work.

  * Allow mouse click+drag movement on both board and mini-map.

* Rework the GUI to use just one <canvas>

* Add (test) authentication for browser clients.

* Add environment object sprites to the board.

* Fix the pixel location detection system and the move to map edge detection
  system, which seem to have gotten messed up by the centering and the right
  resizing revisions.

* Add mouseover information of each hex.
