
import numpy as np
import cv2
import random
import math

SCREENX, SCREENY = 1000, 800

class DancingDot:

    def __init__(self, x, y, size=20, color=(255,255,255), w=0):
        self.xbase = x
        self.ybase = y
        self.size = size
        self.color = color
        self.w = w  # loops from 0..255

    def step(self):
        self.w += 1
        if self.w > 255:
            self.w = 0

    def get_position(self):
        x = self.xbase + int(200 * math.sin(math.pi * self.w / 128.0))
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


dot = DancingDot(500, 400)

while True:
    frame = np.zeros((SCREENY, SCREENX, 3), np.uint8)

    dot.step()
    dot.draw(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
