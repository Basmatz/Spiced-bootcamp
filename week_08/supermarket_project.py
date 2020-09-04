"""
PLAN:
tilemap class: from lesson

customer class
 - self.step (equiv to minute) step.base = 0
 - self.location - categorical (coords in location class??)
        --> location.base = entrance (all customers start at entrance)
- x ,y ??? --> random coords from location (using get_coords)
- self.image (later)

 --- MOVE TO SUPERMARKET CLASS: ----
 - self.supermarket --> customer goes into supermarket (supermarket group class)
    -> change loc method (aisles form supermarket, probabilities from supermarket (current location is an aisle of supermarket - class instance of Location))
        -->time.sleep
    -> leave_shop method?? (if last step takes you to checkout, 2nd iter there takes you off the board

customer group class : simulates a group of customers in a supermarket
 - similar to dotgroup class - introduces customers to shop

location class
    - name (dairy, fruit,drinks, etc. INCLUDES entrance and checkout)
    - limiting coords - from tilemap
    - method get_current_coords (random choice from limiting coords)

supermarket class : makes collection of locations + customer(s)
    - list of locations (list comprehension)
        --> Supermarket()
    - MATRIX GOES HERE (every TP-matrix is supermarket specific)
    - merge with customer group
        self.customers - customers - can append new customers on arrival(?)
            --> -> change loc method (aisles form supermarket, probabilities from supermarket (current location is an aisle of supermarket - class instance of Location))
            -->time.sleep
            -> leave_shop method?? (if last step takes you to checkout, 2nd iter there takes you off the board

        -->
    -
 - potential to expand supermarket easily// model the same supermarket with different conditions (eg. compare days)





"""

"""
MARKET = """
######################
##..................##
##...##...##...##...##
##...##...##...##...##
##...##...##...##...##
##...##...##...##...##
##...##...##...##...##
##..................##
##...##...##...##...##
##...##...##...##...##
##..................##
##....##########....##
##....##########....##
##....##########....##
""".strip()

"""

"""
limits of sections : 
entrance: (11,13), (16,19)
drinks : (1,9),(2,4)
dairy: (1,9), (7,9)
spices: (1,9),(12,14)
fruit: (1,9), (17,19)
checkout: (11, 13), (2,5)
"""


"""
Start with this to implement the simulator.

install OpenCV with:

    pip install opencv-python

"""

import numpy as np
import pandas as pd
import cv2
from random import choices, choice, randint


# P is the Transitional Probability matrix for monday. The first row corresponds to the initial position of each
P= pd.read_csv('matrix.csv')

class Supermarket:
    """Aisles and transitional probabilities have to have the same order!!!!"""
    def __init__(self, customers, aisles, transitional_probabilities):
        self.aisles = aisles
        self.probabilities= transitional_probabilities
        self.customers = customers

    def next_aisle_probabilities(self, current_aisle):
        aisle_vector = np.zeros(len(self.aisles))
        print(type(aisle_vector))
        for i, aisle in enumerate(self.aisles):
            if aisle == current_aisle:
                aisle_vector[i] = 1
                ##print(aisle_vector)
                probabilities_next_aisle = np.dot(aisle_vector, self.probabilities)
        return probabilities_next_aisle

    def move_to_next_aisle(self):
        for customer in self.customers:
            current_aisle = customer.location
            probabilities_next_aisle = next_aisle_probabilities(current_aisle)
            next_location = choices(self.aisles, weights=probabilities_next_aisle, k=1)
            customer.location = next_location





class Location:
    """Creates instances of locations within the supermarket
    name is a string

    x_lims is a tuple pair of limits in x axis
    y_lims is a tuple pair of limits in y axis
    """
    def __init__(self, name, x_lims, y_lims):
        self.name = name
        self.y_lims = y_lims
        self.x_lims = x_lims

    def get_current_coords(self):
        x = randint(self.x_lims[0], self.x_lims[1])
        y = randint(self.y_lims[0], self.y_lims[1])
        return x, y

class Customer:

    def __init__(self, step=0, location='entrance'):
        self.step = step
        self.location = location
        self.coordinates = location.get_current_coords()
        #self.supermarket = supermarket

    def draw(self, frame):
        ...

    def __repr__(self):
        return f"a customer located in the {self.location} aisle after shopping for {step} minutes"

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
        elif char ==
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

sections = {"entrance": {"ylims" :(11,13), "xlims" : (16,19)},
            "drinks" : {"ylims" :(1,9), "xlims" : (2,4)},
            "dairy": {"ylims" :(1,9), "xlims" : (7,9)},
            "spices": {"ylims" :(1,9), "xlims" : (12,14)},
            "fruit": {"ylims" :(1,9), "xlims" : (17,19)},
            "checkout": {"ylims" :(11, 13), "xlims" : (2,5)}
}

aisles = [Location(aisle_name, aisle_coords["ylims"], aisle_coords["xlims"]) for aisle_name, aisle_coords in sections.items()]



background = np.zeros((700, 1000, 3), np.uint8)
tiles = cv2.imread('tiles.png')



market = cv2.imread('supermarket.png')  # a Numpy array with shape (Y, X, 3)

while True:
    frame = market.copy()

    c1.move()
    c1.draw(frame)

    print(c1)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

