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

    board.strokeStyle = '#ffffff';
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
    const HALF_X = 15;
    const MAGIC = [11, 1];

    var border = 10;
    var hex_grid = [40, 40];

    var x_pixels = (hex_grid[X] * HEX_SIZE[X] / 2) + hex_grid[X] * HALF_X + (border * 2) + MAGIC[0];
    var y_pixels = hex_grid[Y] * HEX_SIZE[Y] + HEX_OFFSET[Y] + (border * 2) + MAGIC[1];

    var board = document.getElementById('board');
    board.setAttribute("width", x_pixels);
    board.setAttribute("height", y_pixels);

    var hexagons = [];

    for (var i = 0; i < hex_grid[Y]; i++) {
        x = 0 + border;
        y = i * HEX_SIZE[Y] + border;

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

board()