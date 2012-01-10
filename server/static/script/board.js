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

// Defines the hexagonal board object to be used for the board canvas.
function Board (hex_grid) {
    // Determines the shape of the hexes.
    this.HEX_SIZE   = [57, 54];
    this.HEX_OFFSET = [43, 27];

    // Enhances readability of some of the formulas.
    this.X = 0;
    this.Y = 1;

    // x, y size of the grid.
    this.hex_grid = hex_grid;

    // Current top left location.
    this.x      = 0;
    this.y      = 0;

    // Keeps track of various states.
    this.moved  = false;
    this.gridOn = false;
    this.coords = [false, false];

    // Starts the board set up and drawing.
    this.board = function() {
        // Half of the total hex width, half of the middle (odd) hex width, and an extra 14 gives the max.
        this.x_max = (this.hex_grid[this.X] / 2) * this.HEX_SIZE[this.X] + (this.hex_grid[this.X] / 2) * 29 + 14;

        // The total hex height, plus the y offset, gives the max.
        this.y_max = (this.HEX_SIZE[this.Y] * this.hex_grid[this.Y] + this.HEX_OFFSET[this.Y]);

        this.canvas_set = new setCanvases();

        if (this.x - this.x_height < - this.x_max) {
            this.x = this.x_height - this.x_max;
        }

        this.canvas_set.setAll();

        this.hexSetup();

        // Draws the hexes from the coordinate set, if the grid is on.
        if (this.gridOn == true) {
            this.grid();
        }
    }

    // Sets up the hexagons.
    this.hexSetup = function () {
        var off_x = this.x;
        var off_y = this.y;

        // This holds hexagons, which are lists of six coordinate pairs each.
        this.hexagons = [];

        for (var i = 0; i < this.hex_grid[this.Y]; i++) {
            x = 0 + off_x;
            y = i * this.HEX_SIZE[this.Y] + off_y;

            for (var j = 0; j < this.hex_grid[this.X]; j++) {
                this.hexagons.push(this.getCoords(x, y));
                x += this.HEX_OFFSET[this.X];

                if (j % 2) {
                    y -= this.HEX_OFFSET[this.Y];
                } else {
                    y += this.HEX_OFFSET[this.Y];
                }
            }
        }
    }

    // Draws the grid of hexes.
    this.grid = function () {
        if (this.gridOn == false) {
            this.gridOn = true;
        }

        for (var i = 0; i < this.hexagons.length; i++) {
            this.drawHex(this.hexagons[i]);
        }
    }

    // The lines equation is: y = (y2 - y1) / (x2 - x1) * (x - x1) + y1
    this.diagonal = function (check, pt1, pt2, is_less) {
        if (is_less) {
            return (check[this.Y] < (pt2[this.Y] - pt1[this.Y]) / (pt2[this.X] - pt1[this.X]) * (check[this.X] - pt1[this.X]) + pt1[this.Y]);
        } else {
            return (check[this.Y] > (pt2[this.Y] - pt1[this.Y]) / (pt2[this.X] - pt1[this.X]) * (check[this.X] - pt1[this.X]) + pt1[this.Y]);
        }
    }

    // Determines if points are in a given hex.
    this.isInHex = function (hex_coords, check_coords) {
        // The inside rectangle is the easy case.
        if ((check_coords[this.X] > hex_coords[0][this.X]) &&
            (check_coords[this.X] < hex_coords[1][this.X]) &&
            (check_coords[this.Y] > hex_coords[0][this.Y]) &&
            (check_coords[this.Y] < hex_coords[3][this.Y])) {
            return true;
        }

        // This is the left side triangle.
        else if ((check_coords[this.X] > hex_coords[5][this.X]) &&
                 (check_coords[this.X] < hex_coords[0][this.X]) &&
                 this.diagonal(check_coords, hex_coords[5], hex_coords[0], true) &&
                 this.diagonal(check_coords, hex_coords[5], hex_coords[4], false)) {
            return true;
        }

        // This is the right side triangle.
        else if ((check_coords[this.X] > hex_coords[1][this.X]) &&
                 (check_coords[this.X] < hex_coords[2][this.X]) &&
                 this.diagonal(check_coords, hex_coords[2], hex_coords[1], true) &&
                 this.diagonal(check_coords, hex_coords[2], hex_coords[3], false)) {
            return true;
        }

        else {
            return false;
        }
    }

    // Gets the coordinates for a hexagon based on the shifts.
    this.getCoords = function (x_shift, y_shift) {
        var coords = [[14, 0], [43, 0], [57, 27], [43, 54], [14, 54], [0, 27]];

        for (var i = 0; i < coords.length; i++) {
            coords[i][0] += x_shift;
            coords[i][1] += y_shift;
        }

        return coords;
    }

    // Gets the center of hexagon coordinate list.
    //// todo: This function hasn't been tested.
    this.getCoordCenter = function (hex_coords) {
        return [(hex_coords[0][this.X] + hex_coords[1][this.X]) / 2, hex_coords[2][this.Y]];
    }

    // Draw a hex outline onto a board.
    this.drawHex = function (coords) {
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

// Sets up the canvases that make up the webpage.
function setCanvases() {
    this.x = window.innerWidth;
    this.y = window.innerHeight;

    /*
    try {
        this.player_info = getJSON('players.json');
        this.player = player_info["michael"];
        alert(this.player);
    } catch (e) {
        alert(e.message);
    }
    */

    // Sets all of the canvases.
    this.setAll = function() {
        this.setBoard();
        this.setSidebar();
        this.setFooter();
        this.setHeader();
    }

    // Starts the set up for any canvas.
    this.setStart = function(id, x, y) {
        var canvas = document.getElementById(id);

        canvas.setAttribute("width", x);
        canvas.setAttribute("height", y);

        return canvas.getContext("2d");
    }

    // Sets the center, gameboard canvas.
    this.setBoard = function () {
        board.x_height = this.x - 260;
        board.y_height = this.y - 88;

        var canvas = this.setStart("board", board.x_height, board.y_height);

        // Moves board to the center at the start.
        if (board.moved == false) {
            centerx = - board.x_max / 2;
            centery = - board.y_max / 2;

            board.x = centerx + board.x_height / 2;
            board.y = centery + board.y_height / 2;
        }
    }

    // Sets the sidebar canvas.
    this.setSidebar = function () {
        var canvas = this.setStart("sidebar", 220, this.y - 88);

        var obj = loadImage("static/sphere.png");

        var mini_x = 200;
        var mini_y = 150;

        const mini_corner_x = 10;
        const mini_corner_y = 10;

        canvas.fillStyle = "#333333";
        canvas.fillRect(mini_corner_x, mini_corner_y, mini_x, mini_y);
        canvas.fillRect(10, 195, 50, 50);
        canvas.drawImage(obj, 25, 210);

        var x_ratio = board.x_height / board.x_max;
        var y_ratio = board.y_height / board.y_max;

        var mini_start_x = mini_corner_x - (board.x * ((mini_x - 4) / board.x_max));
        var mini_start_y = mini_corner_y - (board.y * (mini_y / board.y_max));

        canvas.fillStyle = "#000088";
        canvas.fillRect(mini_start_x, mini_start_y, mini_x * x_ratio, mini_y * y_ratio);

        // Provides information of the mouseover hex.
        canvas.fillStyle = "#cccccc";
        canvas.textBaseline = 'top';
        canvas.font = 'bold 14px sans-serif';
        canvas.fillText("Sol", 70, 197);
        canvas.font = 'bold 12px sans-serif';
        canvas.fillText("Star", 70, 217);
        canvas.fillText("Earthlings", 70, 232);

        // Ships
        canvas.drawImage(obj, 15, 167);
        canvas.fillText("4", 40, 171);

        // Fleets
        canvas.drawImage(obj, 85, 167);
        canvas.fillText("1", 110, 171);

        // Territories
        canvas.drawImage(obj, 155, 167);
        canvas.fillText("2", 180, 171);
    }

    // Sets the footer canvas.
    this.setFooter = function () {
        var canvas = this.setStart("footer", this.x - 35, 30);

        canvas.fillStyle = "#cccccc";
        canvas.textBaseline = 'top';
        canvas.font = 'bold 14px sans-serif';
        canvas.textAlign = "center";
        canvas.fillText("May 2500", 50, 7);
        canvas.fillText("Forums", 200, 7);
        canvas.fillText("Wiki", 350, 7);
        canvas.fillText("Developers", 500, 7);
    }

    // Sets the header canvas.
    this.setHeader = function () {
        var xsize = this.x - 35

        var canvas = this.setStart("header", xsize, 30);
        canvas.fillStyle = "#cccccc";
        canvas.textBaseline = 'top';
        canvas.font = 'bold 14px sans-serif';
        icon = loadImage('static/sphere.png');
        canvas.textAlign = "left";

        // Server
        canvas.fillText("Federation", 10, 7);

        if (xsize > 1200) {
            xsize = 1200;
        }

        // Name
        canvas.fillText("Michael (Pirates)", xsize * .16, 7);

        // Credits
        canvas.drawImage(icon, xsize * .45, 3);
        canvas.fillText("200,000", xsize * .45 + 25, 7);

        // Income
        canvas.fillText("(+ 100)", xsize * .45 + 100, 7);

        // Research Points
        canvas.drawImage(icon, xsize * .67, 3);
        canvas.fillText("20", xsize * .67 + 25, 7);

        canvas.textAlign = "right";
        canvas.fillText("(" + board.coords[0] + ", " + board.coords[1] + ")", this.x - 35, 7);
    }
}

// Instantiates the board.
var board = new Board([40, 40]);
