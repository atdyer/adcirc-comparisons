from abc import ABC, abstractmethod

class Shape( ABC ):

    @abstractmethod
    def contains(self, node):
        """Returns true if node falls inside of the shape, false otherwise"""


class InfiniteShape( Shape ):

    def contains(self, node):
        return True

    def __str__(self):
        return "Infinite shape, contains all points"


class Circle( Shape ):

    def __init__( self, x, y, r ):

        self.x = x
        self.y = y
        self.r = r
        self.rsq = r ** 2

    def contains(self, node):
        return ( ( self.x - node[0] ) ** 2 ) + ( ( self.y - node[1] ) ** 2 ) <= self.rsq

    def __str__(self):
        return '<Circle> x: ' + str( self.x ) + ' y: ' + str( self.y ) + ' r: ' + str( self.r )