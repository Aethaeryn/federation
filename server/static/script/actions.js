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

