//    Federation
//    Copyright (C) 2011, 2012 Michael Babich
//
//    Permission is hereby granted, free of charge, to any person obtaining
//    a copy of this software and associated documentation files (the
//    "Software"), to deal in the Software without restriction, including
//    without limitation the rights to use, copy, modify, merge, publish,
//    distribute, sublicense, and/or sell copies of the Software, and to
//    permit persons to whom the Software is furnished to do so, subject to
//    the following conditions:
//
//    The above copyright notice and this permission notice shall be
//    included in all copies or substantial portions of the Software.
//
//    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
//    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
//    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
//    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
//    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


// Turns an image into an object.
function loadImage(location) {
    var img = new Image();
    img.src = location;
    return img;
}

// Draws an image from a sprite sheet onto a canvas.
function drawFromSheet(canvas, image, canvas_x, canvas_y, grid_x, grid_y) {
    // It only works for 28x28 sprites because only that kind exists at the moment.
    const HEIGHT = 28;
    const WIDTH  = 28;

    source_x = WIDTH * (grid_x - 1) + grid_x;
    source_y = HEIGHT * (grid_y - 1) + grid_y;

    canvas.drawImage(image, source_x, source_y, WIDTH, HEIGHT,
                     canvas_x, canvas_y, WIDTH, HEIGHT);
}

// Preloads images for the game board.
function preloader() {
    loadImage("static/sphere.png");
    loadImage("static/icons.png");
}

// Loads json.
function getJSON(location) {
    var file = "data/" + location;

    var foo = $.getJSON(file, function(data, status) {
        //// fixme: Make this work on all JSON data, not just the player named "michael"
        stats = data.michael;

        board.board();
    })


}

var stats = {player : "Anonymous"}

getJSON("player");

// Makes sure the images are loaded into browser cache before used.
preloader();
