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


# Turns an image into an object.
loadImage = (location) ->
  img     = new Image()
  img.src = location
  return img

# Draws an image from a sprite sheet onto a canvas.
# It assumes it's a 28x28 sprite.
drawFromSheet = (canvas, image, canvas_x, canvas_y, grid_x, grid_y) ->
  HEIGHT = 28
  WIDTH  = 28

  source_x = WIDTH * (grid_x - 1) + grid_x
  source_y = HEIGHT * (grid_y - 1) + grid_y

  canvas.drawImage(image, source_x, source_y, WIDTH, HEIGHT, canvas_x, canvas_y, WIDTH, HEIGHT);

# Preloads images for the game board into the browser cache.
preloader = ->
  loadImage("static/sphere.png")
  loadImage("static/icons.png")

stats = {player : "Anonymous"}

# Loads json.
getJSON = (location) ->
  file = "data/" + location;
  foo  = $.getJSON(file, (data, status) ->
    stats = data
    board.board())

#### fixme: generalize this to more players
getJSON("player/michael")

preloader()