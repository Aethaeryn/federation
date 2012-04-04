=========
TODO LIST
=========

Python
------
 * Database code.

   * Every persistent item in the game needs to be in the database,
     unless the item does not change during the game.

   * Needs to interact with game.py, environment.py, and others.

   * Needs to store passwords safely.

 * Authentication and registration needs to be added.

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
