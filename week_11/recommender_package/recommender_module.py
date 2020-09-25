"""
Module Docstring
1. imports
2. Constants
3. classes
4. classless functions
5. if name == main statement

Also use Pylint/ black
"""

import random
import constants

class Recommender:
    """
    A class to logically group all my recommendation functions.
    """

    def __init__(self, items:list):
        self.items = items
        # design decision to pass the list as an argument here (during instantiation)


    def random_recommend(self, n:int = 3) -> list: #type annotation
            """
            Function that returns n elements randomly from a given list.

            Arguments
            ---------
            items: list
            n: int

            Returns
            ---------
            result: list
            """
            result = random.sample(self.items, k=n)
            result = [i.lower() for i in result]
            return result

    def nmf(self):
        """Coming in version 2.0!"""
        pass

    def cosim(self):
        """Coming in version 2.0!"""
        pass



if __name__ == '__main__':

    rec = Recommender(constants.items)
    result = rec.random_recommend(3)
    print(result)
