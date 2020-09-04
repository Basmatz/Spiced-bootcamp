
import numpy as np
import cv2
import random
import math

SCREENX, SCREENY = 1000, 800


class DancingDot:
    """Base class or superclass"""

    def __init__(self, x, y, size=20, color=(255,0,255), w=0):
        self.xbase = x
        self.ybase = y
        self.size = size
        self.color = color
        self.w = w  # loops from 0..255

    def step(self):
        self.w += 2
        if self.w > 255:
            self.w = 0

    def get_position(self):
        x = self.xbase
        y = self.ybase
        return x, y

    def get_boundaries(self, x, y):
        """calculate screen boundaries"""
        x = max(0, x)
        y = max(0, y)
        xmax = min(x + self.size, SCREENX)
        ymax = min(y + self.size, SCREENY)
        return x, y, xmax, ymax

    def draw(self, frame):
        x, y = self.get_position()
        x, y, xmax, ymax = self.get_boundaries(x, y)
        frame[y:ymax, x:xmax] = self.color


class TurquoiseMovingDot(DancingDot):

    def __init__(self, x, y, size=20, w=0):
        self.xbase = x
        self.ybase = y
        self.size = size
        self.color = (209, 206, 0)
        self.w = w  # loops from 0..255

    def get_position(self):
        x = self.xbase + int(200 * math.sin(math.pi * self.w / 128.0))
        y = self.ybase
        return x, y


class RedDancingDot(DancingDot):  # is a special version of DancingDot (subclass)

    def __init__(self, x, y, size=20, w=0):
        self.xbase = x
        self.ybase = y
        self.size = size
        self.color = (0,0,255)
        self.w = w  # loops from 0..255


class GradientDancingDot(DancingDot):

    def step(self):
        self.w += 1
        if self.w > 255:
            self.w = 0
        self.color = (self.w, 0, self.w)

    def get_position(self):
        x = self.xbase + int(200 * math.sin(math.pi * self.w / 128.0))
        y = self.ybase + int(200 * math.sin(math.pi * self.w / 128.0))
        return x, y



class CirlcePathTurquiseDot(TurquoiseMovingDot):  # subclass of a subclass

    def get_position(self):
        x = self.xbase + int(200 * math.sin(math.pi * self.w / 128.0))
        y = self.ybase + int(200 * math.cos(math.pi * self.w / 128.0))
        return x, y


class DotGroup:

    def __init__(self, dots):
        self.dots = dots   # list of DancingDot objects

    def step(self):
        for d in self.dots:
            d.step()

    def draw(self, frame):
        for d in self.dots:
            d.draw(frame)


class GradientDotGroup(DotGroup):

    def set_gradient(self):
        i = 0
        for d in self.dots:
            d.color = (0, 0, i * 20)
            i += 1


dots = [CirlcePathTurquiseDot(x, 600, w=x//3) for x in range(100, 700, 50)]
group = GradientDotGroup(dots)
group.set_gradient()


# create instances
dot = DancingDot(500, 400)
red = RedDancingDot(500, 200)
gra = GradientDancingDot(500, 400)
tur = TurquoiseMovingDot(500, 400)

while True:
    frame = np.zeros((SCREENY, SCREENX, 3), np.uint8)

    dot.step()
    dot.draw(frame)
    red.step()
    red.draw(frame)
    tur.step()
    tur.draw(frame)
    gra.step()
    gra.draw(frame)
    group.step()
    group.draw(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
