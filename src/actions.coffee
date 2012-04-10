#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    This software is licensed under the MIT license.
#    See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php


# Handles the keys.
keyActions = (event) ->
  scroll = 20;

  # Three ways to navigate with the keyboard:
  # UP, DOWN, LEFT, RIGHT; W, S, A, D; K, J, H, L
  up    = [38, 87, 75]
  down  = [40, 83, 74]
  left  = [37, 65, 72]
  right = [39, 68, 76]

  board.moved = true

  if (event.keyCode in up) and (board.y + scroll <= 0)
    board.y += scroll
    board.coords[1] -= scroll

  if event.keyCode in left and (board.x + scroll <= 0)
    board.x += scroll
    board.coords[0] -= scroll

  if event.keyCode in right and (board.x - board.x_height >= - board.x_max)
    board.x -= scroll
    board.coords[0] += scroll

  if event.keyCode in down and (board.y - board.y_height >= - board.y_max)
    board.y -= scroll
    board.coords[1] += scroll

  # 'g' toggles grid
  if event.keyCode is 71
    if board.gridOn is true
      board.gridOn = false
    else
      board.gridOn = true

  # Renders the board again.
  board.board()

# The mouseMove function has been removed until it works again.

window.onresize = (event) ->
  board.board()

window.onload = (event) ->
  board.board()

window.addEventListener('keydown', keyActions, true)
