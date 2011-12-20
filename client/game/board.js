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

function getCoords(x_shift, y_shift) {
    var coords = [[14, 0], [43, 0], [57, 27], [43, 54], [14, 54], [0, 27]];

    for (var i = 0; i < coords.length; i++) {
        coords[i][0] += x_shift;
        coords[i][1] += y_shift;
    }

    return coords;
}

function getCoordCenter(hex_coords) {
    return [(hex_coords[0][0] + hex_coords[1][0]) / 2, hex_coords[2][1]];
}

function draw(coords) {
    var board = document.getElementById('board').getContext('2d');

    board.strokeStyle = '#aaaaaa';
    board.lineWidth = 1;
    board.beginPath();

    board.moveTo(coords[0][0], coords[0][1]);

    for (var i = 1; i < coords.length; i++) {
        board.lineTo(coords[i][0], coords[i][1]);        
    }

    board.closePath();
    board.stroke();
}

function board() {
    const X = 0;
    const Y = 1;

    const HEX_SIZE = [57, 54];
    const HEX_OFFSET = [43, 27];

    var hex_grid = [40, 40];

    var hexagons = [];

    for (var i = 0; i < hex_grid[Y]; i++) {
        x = 0;
        y = i * HEX_SIZE[Y];

        for (var j = 0; j < hex_grid[X]; j++) {
            hexagons.push(getCoords(x, y));
            x += HEX_OFFSET[X];

            if (j % 2) {
                y -= HEX_OFFSET[Y];
            } else {
                y += HEX_OFFSET[Y];
            }
        }
    }

    for (var i = 0; i < hexagons.length; i++) {
        draw(hexagons[i]);
    }
}

function setSize(color) {
    var x_pixels = window.innerWidth;
    var y_pixels = window.innerHeight;

    var board = document.getElementById('board');
    board.setAttribute("width", x_pixels - 260);
    board.setAttribute("height", y_pixels - 88);

    var sidebar = document.getElementById('sidebar');
    sidebar.setAttribute("width", 220);
    sidebar.setAttribute("height", y_pixels - 88);

    side_canvas = sidebar.getContext('2d');
    side_canvas.fillStyle = "#888888";
    side_canvas.fillRect(0, 0, 220, y_pixels - 88);

    side_canvas.fillStyle = color;

    side_canvas.fillRect(10, 10, 200, 150);

    side_canvas.fillRect(10, 165, 50, 50);

    var footer = document.getElementById('footer');

    footer.setAttribute("width", x_pixels - 35);
    footer.setAttribute("height", 30);

    foot_canvas = footer.getContext('2d');
    foot_canvas.fillStyle = "#888888";
    foot_canvas.fillRect(0, 0, x_pixels - 35, 30);

    var header = document.getElementById('header');

    header.setAttribute("width", x_pixels - 35);
    header.setAttribute("height", 30);

    head_canvas = header.getContext('2d');
    head_canvas.fillStyle = "#888888";
    head_canvas.fillRect(0, 0, x_pixels - 35, 30);
}

window.onresize = function(event) {
    setSize("#333333");
}

function keyActions(event) {
    switch (event.keyCode) {
    case 37: // left
        setSize("#000000");
        break;
    case 38: // up
        setSize("#0000ff");
        break;
    case 39: // right
        setSize("#ff0000");
        break;
    case 40: //down
        setSize("#00ff00");
        break;
    case 71: // 'g'
        board();
        break;
    }
}

window.addEventListener('keydown', keyActions, true);

setSize("#333333");