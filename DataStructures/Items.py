from abc import ABC, abstractmethod

class Item(ABC):

    @abstractmethod
    def is_inside(self, quad):
        """Returns true if the item falls inside of the quadtree"""

class Point(Item):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self, quad):
        return (quad.x_range[0] <= self.x < quad.x_range[1] and
                quad.y_range[0] <= self.y < quad.y_range[1])

class Node(Item):

    def __init__(self, x, y, z=None, node_number=None ):
        self.x = x
        self.y = y
        self.z = z
        self.node_number = node_number

    def is_inside(self, quad):
        return (quad.x_range[0] <= self.x < quad.x_range[1] and
                quad.y_range[0] <= self.y < quad.y_range[1])

class MeshNode(Item):

    def __init__(self, mesh, node_number ):
        self.node_number = node_number
        self.mesh = mesh

    def is_inside(self, quad):
        return (quad.x_range[0] <= self.mesh.nodes[self.node_number][0] < quad.x_range[1] and
                quad.y_range[0] <= self.mesh.nodes[self.node_number][1] < quad.y_range[1])

class Element(Item):

    def __init__(self, n1: Node, n2: Node, n3:Node):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

    def is_inside(self, quad):
        return self.n1.is_inside(quad) or self.n2.is_inside(quad) or self.n3.is_inside(quad)

class MeshElement(Item):

    def __init__(self, mesh, element_number):
        self.element_number = element_number
        self.mesh = mesh

    def is_inside(self, quad):
        e = self.mesh.elements[ self.element_number ]

        n1 = e[0]
        n2 = e[1]
        n3 = e[2]

        x1, y1, _ = self.mesh.nodes[n1]
        x2, y2, _ = self.mesh.nodes[n2]
        x3, y3, _ = self.mesh.nodes[n3]

        return ((quad.x_range[0] <= x1 < quad.x_range[1] and quad.y_range[0] <= y1 < quad.y_range[1]) or
                (quad.x_range[0] <= x2 < quad.x_range[1] and quad.y_range[0] <= y2 < quad.y_range[1]) or
                (quad.x_range[0] <= x3 < quad.x_range[1] and quad.y_range[0] <= y3 < quad.y_range[1]))
