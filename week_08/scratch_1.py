import numpy as np
from random import randint

class Supermarket:
    """Aisles and transitional probabilities have to have the same order!!!!"""
    def __init__(self, aisles, transitional_probabilities, customers):
        self.aisles = aisles #instances of Location class
        self.probabilities= transitional_probabilities
        self.customers = customers #collection of instances of Customer()

    def next_aisle_probabilities(self, current_aisle):
        aisle_vector = np.zeros(len(self.aisles))
        print(type(aisle_vector))
        for i, aisle in enumerate(self.aisles):
            if aisle == current_aisle:
                aisle_vector[i] = 1
                print(aisle_vector)

                probabilities_next_aisle = np.dot(aisle_vector, self.probabilities)
        return probabilities_next_aisle

    def move_to_next_aisle(self):
        for customer in self.customers:
            current_aisle = customer.location
            probabilities_next_aisle = self.next_aisle_probabilities(current_aisle)
            next_location = choices(self.aisles, weights=probabilities_next_aisle, k=1)
            customer.location = next_location


probs = np.array([0.3, 0.3, 0.4,1,0,0,0.5,0.2,0.3]).reshape(3,3)
sections = {"entrance": {"ylims" :(11,13), "xlims" : (16,19)},
            "drinks" : {"ylims" :(1,9), "xlims" : (2,4)},
            "dairy": {"ylims" :(1,9), "xlims" : (7,9)},
            "spices": {"ylims" :(1,9), "xlims" : (12,14)},
            "fruit": {"ylims" :(1,9), "xlims" : (17,19)},
            "checkout": {"ylims" :(11, 13), "xlims" : (2,5)}
}


class Location:
    """Creates instances of locations within the supermarket
    name is a string

    x_lims is a tuple pair of limits in x axis
    y_lims is a tuple pair of limits in y axis
    """
    def __init__(self, name, ylims, xlims):
        self.name = name
        self.ylims = ylims
        self.xlims = xlims

    def get_current_coords(self):
        x = randint(self.xlims[0],self.xlims[1] )
        y = randint(self.ylims[0],self.ylims[1] )
        return x, y

class Customer:

    def __init__(self, location, step=0):
        self.step = step
        self.location = location
        self.coordinates = location.get_current_coords()
        #self.supermarket = supermarket

    def draw(self, frame):
        ...

    def __repr__(self):
        return f"a customer located in the {self.location} aisle after shopping for {step} minutes"



aisles = [Location(aisle_name, aisle_coords["ylims"], aisle_coords["xlims"]) for aisle_name, aisle_coords in sections.items()]
susan = Customer(location=aisles[0])
bob = Customer(location=aisles[2])

customers = [susan, bob]

supermarket= Supermarket(aisles=aisles, transitional_probabilities=probs, customers=customers)

print([customer.location.get_current_coords() for customer in supermarket.customers])
supermarket.move_to_next_aisle()
print([customer.location.get_current_coords() for customer in supermarket.customers])