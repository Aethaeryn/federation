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

function Board () {
    this.moved = false;
    this.x = 0;
    this.y = 0;

    this.board = function() {
        const X = 0;
        const Y = 1;

        const HEX_SIZE = [57, 54];
        const HEX_OFFSET = [43, 27];

        var hex_grid = [40, 40];

        // Half of the total hex width, half of the middle (odd) hex width, and an extra 14 gives the max.
        this.x_max = (hex_grid[X] / 2) * HEX_SIZE[X] + (hex_grid[X] / 2) * 29 + 14;

        // The total hex height, plus the y offset, gives the max.
        this.y_max = (HEX_SIZE[Y] * hex_grid[Y] + HEX_OFFSET[Y]);

        /* fixme: code to center the board on start
           if (this.moved == false) {
           this.x = - this.x_max / 2;
           this.y = - this.y_max / 2;
           } */

        var off_x = this.x;
        var off_y = this.y;

        setSize("#333333");

        this.hexagons = [];

        for (var i = 0; i < hex_grid[Y]; i++) {
            x = 0 + off_x;
            y = i * HEX_SIZE[Y] + off_y;

            for (var j = 0; j < hex_grid[X]; j++) {
                this.hexagons.push(this.getCoords(x, y));
                x += HEX_OFFSET[X];

                if (j % 2) {
                    y -= HEX_OFFSET[Y];
                } else {
                    y += HEX_OFFSET[Y];
                }
            }
        }

        this.grid();
    }

    this.grid = function () {
        for (var i = 0; i < this.hexagons.length; i++) {
            this.drawGrid(this.hexagons[i]);
        }
    }

    this.getCoords = function (x_shift, y_shift) {
        var coords = [[14, 0], [43, 0], [57, 27], [43, 54], [14, 54], [0, 27]];

        for (var i = 0; i < coords.length; i++) {
            coords[i][0] += x_shift;
            coords[i][1] += y_shift;
        }

        return coords;
    }

    this.getCoordCenter = function (hex_coords) {
        return [(hex_coords[0][0] + hex_coords[1][0]) / 2, hex_coords[2][1]];
    }

    this.drawGrid = function (coords) {
        var board_canvas = document.getElementById('board').getContext('2d');

        board_canvas.strokeStyle = '#aaaaaa';
        board_canvas.lineWidth = 1;
        board_canvas.beginPath();

        board_canvas.moveTo(coords[0][0], coords[0][1]);

        for (var i = 1; i < coords.length; i++) {
            board_canvas.lineTo(coords[i][0], coords[i][1]);        
        }

        board_canvas.closePath();
        board_canvas.stroke();
    }
}

var board = new Board();

function setSize(color) {
    var x_pixels = window.innerWidth;
    var y_pixels = window.innerHeight;

    var board_canvas = document.getElementById('board');
    board_canvas.setAttribute("width", x_pixels - 260);
    board_canvas.setAttribute("height", y_pixels - 88);

    board.y_height = y_pixels - 88;
    board.x_height = x_pixels - 260;

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
    board.board();
}

window.onload = function(event) {
    board.board();
}

function keyActions(event) {
    const SCROLL = 20;

    board.moved = true;

    // Left scrolls left.
    if (event.keyCode == 37) {
        if (board.x + SCROLL <= 0) {
            board.x += SCROLL;
        }
    }

    // Up scrolls up.
    if (event.keyCode == 38) {
        if (board.y + SCROLL <= 0) {
            board.y += SCROLL;
        }
    }

    // Right scrolls right.
    if (event.keyCode == 39) {
        if (board.x - board.x_height >= - board.x_max) {
            board.x -= SCROLL;
        }
    }

    // Down scrolls down.
    if (event.keyCode == 40) {
        if (board.y - board.y_height >= - board.y_max) {
            board.y -= SCROLL;
        }
    }

    board.board();

    /*
    switch (event.keyCode) {
    case 71: // 'g'
        break;
    }
    */
}

// Accurately captures location of mouse on board canvas.
function mouseMove(event) {
    var x = event.clientX - 10 - board.x;
    var y = event.clientY - 45 - board.y;

    if (x < 0 || x > board.x_height) {
        x = false;
    }

    if (y < 0 || y > board.y_height) {
        y = false;
    }

    // alert(x + ', ' + y);
}

window.addEventListener('keydown', keyActions, true);
document.addEventListener('mousemove', mouseMove, true)
