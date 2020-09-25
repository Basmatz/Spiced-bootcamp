
import numpy as np
import cv2
import random

TILE_SIZE = 32
OFS = 50

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..#b..##
##..##..##..##..##
##..##..##..#b..##
##..##..##..##..##
##...............#
##..##..##..##...#
##..##..##..##...#
##...............#
##################
""".strip()


class TiledMap:

    def __init__(self, layout, tiles):
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split('\n')]
        self.xsize =  len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros((self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8)
        self.prepare_map()

    def get_tile_bitmap(self, char):
        if char == '#':
            return self.tiles[0:32, 0:32, :]

        elif char == 'b':
            return self.tiles[0:32, -32:, :]

        else:
            return self.tiles[32:64, 64:96, :]

    def prepare_map(self):
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile_bitmap(tile)
                self.image[y * TILE_SIZE:(y+1)*TILE_SIZE,
                      x * TILE_SIZE:(x+1)*TILE_SIZE] = bm

    def draw(self, frame):
        frame[OFS:OFS+self.image.shape[0], OFS:OFS+self.image.shape[1]] = self.image


class Customer:

    def __init__(self, tmap, image, x, y):
         self.tmap = tmap
         self.image = image
         self.x = x
         self.y = y

    def draw(self, frame):
        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
        frame[ypos:ypos + TILE_SIZE, xpos: xpos + TILE_SIZE] = self.image

    def move(self, direction):
        newx = self.x
        newy = self.y
        if direction == 'up':
            newy -= 1
        elif direction == 'down':
            newy += 1
        elif direction == 'left':
            newx -= 1
        elif direction == 'right':
            newx += 1

        if self.tmap.contents[newy][newx] == '.':
            self.x = newx
            self.y = newy

    def __repr__(self):
        return f"This is a customer at position {self.y}, {self.x}."





background = np.zeros((700, 1000, 3), np.uint8)
tiles = cv2.imread('tiles.png')

tmap = TiledMap(MARKET, tiles)

customer_image = tiles[-2*TILE_SIZE:-1*TILE_SIZE, :1*TILE_SIZE, :]

c = Customer(tmap, customer_image, 15, 10)

while True:
    frame = background.copy()
    tmap.draw(frame)
    c.draw(frame)

    cv2.imshow('frame', frame)

    key = chr(cv2.waitKey(1) & 0xFF)

    if key == 'w':
        c.move('up')
    if key == 's':
        c.move('down')
    if key == 'a':
        c.move('left')
    if key == 'd':
        c.move('right')
    if key == 'q':
        break


cv2.destroyAllWindows()
