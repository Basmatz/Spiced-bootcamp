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
    def __init__(self, name, x_lims, y_lims):
        self.name = name
        self.y_lims = y_lims
        self.x_lims = x_lims

    def get_current_coords(self):
        x = randint(self.x_lims[0], self.x_lims[1])
        y = randint(self.y_lims[0], self.y_lims[1])
        return x, y



#for aisle_name, aisle_coords in sections.items():
#    location = Location(aisle_name, aisle_coords["ylims"], aisle_coords["xlims"])


aisles = [Location(aisle_name, aisle_coords["ylims"], aisle_coords["xlims"]) for aisle_name, aisle_coords in sections.items()]

print([aisle.name for aisle in aisles])