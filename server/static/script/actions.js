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

// Handles keys.
function keyActions(event) {
    // Sets the scroll rate.
    const SCROLL = 20;

    board.moved = true;

    // Left scrolls left.
    if (event.keyCode == 37) {
        if (board.x + SCROLL <= 0) {
            board.x += SCROLL;
            board.coords[0] -= SCROLL;
        }
    }

    // Up scrolls up.
    if (event.keyCode == 38) {
        if (board.y + SCROLL <= 0) {
            board.y += SCROLL;
            board.coords[1] -= SCROLL;
        }
    }

    // Right scrolls right.
    if (event.keyCode == 39) {
        if (board.x - board.x_height >= - board.x_max) {
            board.x -= SCROLL;
            board.coords[0] += SCROLL;
        }
    }

    // Down scrolls down.
    if (event.keyCode == 40) {
        if (board.y - board.y_height >= - board.y_max) {
            board.y -= SCROLL;
            board.coords[1] += SCROLL;
        }
    }

    // Reads the other keys that do actions.
    switch (event.keyCode) {
    case 71: // 'g'
        if (board.gridOn == true) {
            board.gridOn = false;
        } else {
            board.gridOn = true;
        }

        break;
    }

    // Rerenders the board.
    board.board();
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

    if (x != false && y != false) {
        board.coords[0] = x;
        board.coords[1] = y;

        board.canvas_set.setHeader();
    }
}

// The rest of the file listens for various events.
window.onresize = function(event) {
    board.board();
}

window.onload = function(event) {
    board.board();
}

window.addEventListener('keydown', keyActions, true);
document.addEventListener('mousemove', mouseMove, true)

