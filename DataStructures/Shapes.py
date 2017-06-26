from abc import ABC, abstractmethod
from .Items import *

class Shape(ABC):

    @abstractmethod
    def contains(self, item: Item):
        """Returns true if this shape contains the item"""

    @abstractmethod
    def intersects(self, x1, y1, x2, y2):
        """Returns true if a line segment intersects with the shape's edge"""

    @abstractmethod
    def edge_point(self):
        """Returns a single point that falls on the edge of this shape"""

class PointShape(Shape):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def contains(self, item: Item):
        if type(item) is Point:
            return item.x == self.x and item.y == self.y
        if type(item) is Node:
            return item.x == self.x and item.y == self.y
        if type(item) is MeshElement:
            nodes = item.mesh.elements[item.element_number]
            p0 = item.mesh.nodes[nodes[0]]
            p1 = item.mesh.nodes[nodes[1]]
            p2 = item.mesh.nodes[nodes[2]]

            s = p0[1] * p2[0] - p0[0] * p2[1] + (p2[1] - p0[1]) * self.x + (p0[0] - p2[0]) * self.y
            t = p0[0] * p1[1] - p0[1] * p1[0] + (p0[1] - p1[1]) * self.x + (p1[0] - p0[0]) * self.y
            
            if s < 0 != t < 0:
                return False

            a = -p1[1] * p2[0] + p0[1] * (p2[0] - p1[0]) + p0[0] * (p1[1] - p2[1]) + p1[0] * p2[1]
            if a < 0.0:
                s = -s
                t = -t
                a = -a

            return s > 0.0 and t > 0.0 and s + t <= a

    def intersects(self, x1, y1, x2, y2):
        return False

    def edge_point(self):
        return self.x, self.y