import Image, ImageDraw, sys

class Hex():
    def __init__(self, x_shift, y_shift):
        # These are the coordinates of the upper left hex. All other coordinates are shifted.
        self. points = [[14, 0], [43, 0], [57, 27], [43, 54], [14, 54], [0, 27]]

        for point in self.points:
            point[0] += x_shift
            point[1] += y_shift

    # Draws lines through every adjacent point in the hexagon.
    def draw(self, img):
        for i in range(6):
            start = i
            if i != 5:
                end = i + 1
            else:
                end = 0

            img.line([self.points[start][0], self.points[start][1], self.points[end][0], self.points[end][1]])

class Board():
    def __init__(self, hex_grid, border):
    # Gets index positions to act like x/y coordinates.
    X = 0
    Y = 1

    # * These constants make generating work. Do not mess with them unless you know what you're doing. * #
    # Size of the hexes.
    HEX_SIZE   = (57, 54)

    # Offsets each X and every other Y.
    HEX_OFFSET = (43, 27)

    # Space between the even Xs.
    HALF_X     = 15

    # Magicly fixes the x_pixels and y_pixels calculations for any border size.
    MAGIC      = (11, 1)

    # Sets up the board sizejmnk in pixels.
    x_pixels   = (hex_grid[X] * HEX_SIZE[X] / 2) + hex_grid[X] * HALF_X + (border * 2) + MAGIC[0]
    y_pixels   = hex_grid[Y] * HEX_SIZE[Y] + HEX_OFFSET[Y] + (border * 2) + MAGIC[1]
    board_size = (x_pixels, y_pixels)

    # Fills a hexagon list with Hex objects with pixel coordinates.
    hexagons = []

    for i in range(hex_grid[Y]):
        x = 0 + border
        y = i * HEX_SIZE[Y] + border

        for j in range(hex_grid[X]):
            hexagons.append(Hex(x, y))
            x += HEX_OFFSET[X]

            if j % 2: y -= HEX_OFFSET[Y]
            else: y += HEX_OFFSET[Y]

    # Draws the hexagons onto a test.png.
    img = Image.new("RGB", board_size)

    draw = ImageDraw.Draw(img)

    for hexagon in hexagons:
        hexagon.draw(draw)

    img.save("test.png", "PNG")      

def main():
    # Variables.
    hex_grid   = (10, 5)
    border     = 10

    board = Board(hex_grid, border)

main()
