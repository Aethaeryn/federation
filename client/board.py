import Image, ImageDraw, sys

class Hex():
    def __init__(self, x_shift, y_shift):
        self. points = [[14,  0], [43,  0], [57, 27], [43, 54], [14, 54], [ 0, 27]]

        for point in self.points:
            point[0] += x_shift
            point[1] += y_shift

    def draw(self, img):
        for i in range(6):
            start = i
            if i != 5:
                end = i + 1
            else:
                end = 0

            img.line([self.points[start][0], self.points[start][1], self.points[end][0], self.points[end][1]])

def main():
    X = 0
    Y = 1

    hexagons = []

    HEX_GRID   = (10, 5)
    border     = (10, 10)

    HEX_SIZE   = (57, 54)
    HEX_OFFSET = (43, 27)
    
    x_pixels   = HEX_GRID[X] * HEX_SIZE[X] + HEX_OFFSET[X] + (border[X] * 2) + 1
    y_pixels   = HEX_GRID[Y] * HEX_SIZE[Y] + HEX_OFFSET[Y] + (border[Y] * 2) + 1

    BOARD_SIZE = (x_pixels, y_pixels)

#    BOARD_SIZE = (HEX_GRID[0] * 57 + border * 2 - ((HEX_GRID[0] - 1 / 2) * 11),
#                  HEX_GRID[1] * 54 + 27 + border * 2 + 1)

    for i in range(HEX_GRID[Y]):
        x = 0 + border[X]
        y = i * HEX_SIZE[Y] + border[Y]

        for j in range(HEX_GRID[X]):
            hexagons.append(Hex(x, y))
            x += HEX_OFFSET[0]

            if j % 2: y -= HEX_OFFSET[1]
            else: y += HEX_OFFSET[1]

    img = Image.new("RGB", BOARD_SIZE)

    draw = ImageDraw.Draw(img)

    for hexagon in hexagons:
        hexagon.draw(draw)

    img.save("test.png", "PNG")

main()
