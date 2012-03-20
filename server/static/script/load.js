//    Federation
//    Copyright (C) 2011, 2012 Michael Babich
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
