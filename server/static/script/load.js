//    Federation
//    Copyright (C) 2011 Michael Babich
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

// Preloads images for the game board.
function preloader() {
    loadImage("static/sphere.png");
    loadImage("static/icons.png");
}

// Loads json.
function getJSON(location) {
    var file = "data/" + location;

    $.getJSON(file, function(data, status) {
        alert(data);
    })
}

getJSON("environment");

// Makes sure the images are loaded into browser cache before used.
preloader();
