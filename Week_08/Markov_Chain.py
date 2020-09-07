#%% md

# Project: Markov Simulation

#%% md

### Imports

#%%

import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import random as rd
import time
import cv2
import numpy as np

prob_first = pd.read_csv("prob_first.csv", index_col="location")
prob_following = pd.read_csv("prob_following.csv", index_col="location")

#%% md

### Monte Carlo simulation

#%%

TILE_SIZE = 32
OFS = 5
INITIAL_STATE = "entrance"
FINAL_STATE = "checkout"
END = 0

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..#e..p#
##..##..##..#b..m#
##..##..##..#c..k#
##..##..##..##..##
##...............#
##..##..##..##...#
##..##..##..##...#
##...............#
##################
""".strip()

class Customer:
    '''
    The class Customer is a blueprint for a supermarket customer

    Parameters
    ----------
    name: Name String of the customer
    sex: Gender of customer
    age: Age in years of customer
    '''

    def __init__(self, image):
        self.state = INITIAL_STATE
        self.result = []
        self.image = image.copy()
        self.image[:,:, 2] = np.random.randint(256)
        self.x = 15
        self.y = 10
        self.exit = 0

    def __repr__(self):
        return f"Supermarket customer"

    def go_shopping(self):
        while self.state != FINAL_STATE:
            if self.state == INITIAL_STATE:
                self.result.append(self.state)
                self.state = rd.choices(list(prob_first.index.values), weights= list(prob_first[self.state].values))[0]
            else:
                self.state = rd.choices(list(prob_following.index.values), weights= list(prob_following[self.state].values))[0]
            self.result.append(self.state)
            #print(f"{self.name} is now in the {self.state} section")
            time.sleep(1)
        #print(f"The customer {self.name}, {self.age}y/o, {self.sex} entered the supermarket")
        return #self.result

    def draw(self, frame):
        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
        global END

        if self.state != FINAL_STATE:
            if self.state == INITIAL_STATE:
                #print(f"Customer {self.name}, {self.age}y/o, {self.sex} entered the supermarket")
                self.result.append(self.state)
                self.state = rd.choices(list(prob_first.index.values), weights=list(prob_first[self.state].values))[0]
            else:
                #print(f"{self.name} is now in the {self.state} section")
                self.state = rd.choices(list(prob_following.index.values), weights=list(prob_following[self.state].values))[0]
            self.result.append(self.state)


            if self.state == "entrance":
                self.x = np.random.randint(11,17)
                self.y = 10
            if self.state == "fruit":
                self.x = np.random.randint(14,16)
                self.y = np.random.randint(1,10)
            if self.state == "dairy":
                self.x = np.random.randint(10,12)
                self.y = np.random.randint(1,10)
            if self.state == "drinks":
                self.x = np.random.randint(6,8)
                self.y = np.random.randint(1,10)
            if self.state == "spices":
                self.x = np.random.randint(2,4)
                self.y = np.random.randint(1,10)
            if self.state == "checkout":
                self.x = np.random.randint(2,10)
                self.y = 10
                #print(f"The customer {self.name} went after {len(self.result) - 1} minutes to the checkout")

        if self.state == "checkout" and self.exit < 6:
            self.exit += 1
            END = 0

        if self.exit <= 5:
            frame[ypos: ypos + self.image.shape[0], xpos: xpos + self.image.shape[1]] = self.image
            END += 1


        # print(f"{self.name} is now in the {self.state} section")
        # time.sleep(1)
        # frame[y * TILE_SIZE:(y + 1) * TILE_SIZE, x * TILE_SIZE:(x + 1) * TILE_SIZE] = self.image
        # self.image[y * TILE_SIZE:(y + 1) * TILE_SIZE, x * TILE_SIZE:(x + 1) * TILE_SIZE] = self.image

        #frame[y:y + self.image.shape[0], x:x + self.image.shape[1]] = self.image

        # if i%2==0:
        #     frame[ypos:ypos+TILE_SIZE, xpos: xpos+TILE_SIZE] = self.image[0]
        # else:
        #     frame[ypos:ypos+TILE_SIZE, xpos: xpos+TILE_SIZE] = self.image[1]

#%%

class Supermarket:
    '''
    The class Supermaket generates a visualization of a supermarket
    '''

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
        if char == "e":
            return self.tiles[0:32, -32:, :]
        if char == "p":
            return self.tiles[0:32, -32:, :]
        if char == "b":
            return self.tiles[0:32, -32:, :]
        if char == "m":
            return self.tiles[0:32, -32:, :]
        if char == "c":
            return self.tiles[0:32, -32:, :]
        if char == "k":
            return self.tiles[0:32, -32:, :]
        else:
            return self.tiles[32:64, 64:96, :]

    def prepare_map(self):
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile_bitmap(tile)
                self.image[y * TILE_SIZE:(y+1)*TILE_SIZE, x * TILE_SIZE:(x+1)*TILE_SIZE] = bm

    def draw(self, frame):
        frame[OFS:OFS+self.image.shape[0], OFS:OFS+self.image.shape[1]] = self.image



#%%


background = np.zeros((394, 586, 3), np.uint8)
tiles = cv2.imread('tiles.png')

tmap = Supermarket(MARKET, tiles)

bunch = [Customer(tiles[96:128, :32, :]) for c in range(100)]
# c1 = Customer(tiles[96:128, :32, :], 255)
# c2 = Customer(tiles[96:128, :32, :], 180)

while END >= -2:

    frame = background.copy()
    tmap.draw(frame)



    for c in bunch:
        c.draw(frame)
    # c1.draw(frame)
    # c2.draw(frame)

    cv2.imshow('frame', frame)
    time.sleep(0.5)

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

    END -= 1

cv2.destroyAllWindows()