#    Federation
#    Copyright (C) 2011, 2012 Michael Babich
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files (the
#    "Software"), to deal in the Software without restriction, including
#    without limitation the rights to use, copy, modify, merge, publish,
#    distribute, sublicense, and/or sell copies of the Software, and to
#    permit persons to whom the Software is furnished to do so, subject to
#    the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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
