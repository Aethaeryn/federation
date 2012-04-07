=========
TODO LIST
=========

Python
------
* Game elements.

  * Map generation.

  * A location system.

  * Territories and bodies.

    * Ownership and stats.

* db <---> game <---> json

  * Spacecraft and components: individual "instances".

  * Structure, Unit, Body, Map (System, Sector)

* Authentication and registration needs to be added.

  * Extend player code in db to store passwords safely.

* Hex calculation algorithms.

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
