# Copyright (c) 2011, 2012 Michael Babich
# See LICENSE.txt or http://www.opensource.org/licenses/mit-license.php

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
  loadImage('static/sphere.png')
  loadImage('static/icons.png')

stats = {player : 'Anonymous'}

# Loads json.
getJSON = (location) ->
  file = 'data/' + location;
  foo  = $.getJSON(file, (data, status) ->
    stats = data
    board.board())

#### fixme: generalize this to more players
getJSON('player/michael')

preloader()
