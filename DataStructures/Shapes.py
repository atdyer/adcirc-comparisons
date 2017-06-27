from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def contains_point(self, x, y):
        """Returns True if the point (x, y) falls inside of the shape, False otherwise"""

class Circle(Shape):

    def __init__(self, x, y, r):

        self.x = x
        self.y = y
        self.r = r
        self.rsq = r*r

    def contains_point(self, x, y):

        return ((self.x - x)**2 + (self.y - y)**2) <= self.rsq

class Infinite(Shape):

    def contains_point(self, x, y):

        return True