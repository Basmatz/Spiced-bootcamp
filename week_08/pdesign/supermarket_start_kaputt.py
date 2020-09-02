"""
    pip install opencv-python
"""

import numpy as np
import cv2
import random    
    
class Location:

    def __init__(self, name, x, y, n_customers=3):
        # set attributes of the class
        self.name = name # name : string, for debugging
        self.x = x # x : x-position of the location
        self.y = y # y : y-position of the location
        self.n_customers = n_customers # n_customers currently in that location
        ...

    def __repr__(self):
        """return a string, good for debugging."""
        return f"The location is {self.name} at x/y {self.x}/{self.y} with {self.n_customers} customers."

    def draw(self, frame):
        """draws n_customers onto the frame"""
        #array = np.arange(self.n_customers)
        for i in range(self.n_customers):
         #   frame[self.x + 10:self.x + 20, self.y + 10 * array[i]:self.y + 10 * array[i] + 20] = (255, 0, 128)
        #frame[self.x:self.x + 20, self.y:self.y+20] = (255, 100, 128)
            cblock = 20
            nextblock = 30
            frame[self.x + nextblock*i:self.x + nextblock*i + cblock, self.y:self.y + cblock] = (200, 100, 128)
        #frame[self.x + block*3:self.x + block*3 + block, self.y:self.y + block] = (200, 100, 128)
        #frame[self.x + block*4:self.x + block*4 + block, self.y:self.y + block] = (200, 100, 128)
        #frame[self.x + block*5:self.x + block*5 + block, self.y:self.y + block] = (200, 100, 128)
            #frame[self.x:self.x + 20, self.y:self.y+20] = (255, 100, 128)
            
            
class Customer:

    def __init__(self, location = Location('entrance', 650, 800)):
        #self.x = x
        #self.y = y
        #self.color = color
        self.location = location
        

    def draw(self, frame):
        frame[self.x:self.x + 20,self.y:self.y+20] = self.color

    def move(self):
        """somehow figures out itself where it has to go"""
        #self.x += random.randint(-1, 1)
        #self.y += random.randint(-1, 1)
        old_location = self.location
        new_location = Location('dairy', 300, 400)
        new_location.n_customers += 1
        #self.location = str(location)
        #return location.n_customers + 1 
        

    def __repr__(self):
        return "" #f"customer at {self.x}/{self.y}"



pink = (255, 0, 128)
#c1 = Customer(100, 100, pink)
#c2 = Customer(500, 500, (0, 255, 0))
c1 = Customer()

market = cv2.imread('market.png')  # a Numpy array with shape (Y, X, 3)

drinks = Location('dairy', 300, 200)
dairy = Location('dairy', 300, 400)
spices = Location('spices', 300, 600)
fruit = Location('spices', 300, 800)
checkout = Location('dairy', 650, 200)


while True:
    frame = market.copy()

    c1.move()
    #spices.n_customers = random.randint(0, 5)
    #dairy.n_customers = random.randint(0, 3)
    #c1.draw(frame)
    drinks.draw(frame)
    dairy.draw(frame)
    spices.draw(frame)
    fruit.draw(frame)
    checkout.draw(frame)
    

    #print(spices)
    #c2.move()
    #spices.draw()
    #print(spices)
    #c2.draw(frame)
    #print(c1)
    
    

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
