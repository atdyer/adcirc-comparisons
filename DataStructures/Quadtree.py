from .Utilities import point_in_triangle

class Quadtree:

    def __init__(self, mesh, bin_size, x_range=None, y_range=None, parent=None):

        """Initializes an empty quadtree.

        The x_range and y_range tuples describe the spatial extent
        of the quadtree, and the bin_size is the maximum number
        of items allowed in a leaf before it splits into a branch.
        A quadtree without a parent is considered the root branch
        of the tree.
        """

        # The mesh
        self.mesh = mesh

        # The data ranges
        self.x_range = x_range if x_range is not None else mesh.x_bounds()
        self.y_range = y_range if y_range is not None else mesh.y_bounds()

        # The maximum number of Items that a leaf can hold
        self.bin_size = bin_size

        # The parent of this Quad (None if this is the top of the tree)
        self.parent = parent

        # Children will be a list of Quadtrees
        self._children = None

        # How deep into the tree are we?
        self._depth = 0 if parent is None else 1 + parent.depth()

        # The data contained by this leaf (if this is a leaf)
        self._data = []

        # Build the quadtree if this is the root quad
        if parent is None:
            self.add_elements()


    def add_elements(self):
        """Adds all elements of a mesh to a quadtree"""

        for element_number, _ in self.mesh.elements():

            self.add_element(element_number)


    def add_element(self, element_number):
        """Adds a single element to the quadtree"""

        # Is this a branch?
        if self._children is not None:

            # Yes, so find the child(ren) it falls into
            for child in self._children:

                if child.contains_element(element_number):

                    child.add_element(element_number)

        else:

            # No, so either add the item to this leaf or split this leaf into a branch
            if self.contains_element(element_number):

                if len( self._data ) >= self.bin_size:

                    self._branch()
                    self.add_element(element_number)

                else:

                    self._data.append(element_number)

    def depth(self):

        return self._depth

    def find_element(self, x, y):

        # Check if this is a branch
        if self._children is not None:

            # It is, so recurse through children
            for child in self._children:

                if child.contains_point(x, y):

                    return child.find_element(x, y)

        else:

            # It isn't, so look through the data
            for element in self._data:

                n1, n2, n3 = self.mesh.element(element)
                x1, y1, _ = self.mesh.node(n1)
                x2, y2, _ = self.mesh.node(n2)
                x3, y3, _ = self.mesh.node(n3)

                if point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
                    return element

    def max_depth(self):

        if self._children is not None:

            return max([child.max_depth() for child in self._children])

        else:

            return self._depth



    def _branch(self):

        # Find the centerpoint
        center_x = (self.x_range[0] + self.x_range[1]) / 2.0
        center_y = (self.y_range[0] + self.y_range[1]) / 2.0

        # Create the children
        ll = Quadtree(self.mesh, self.bin_size, (self.x_range[0], center_x), (self.y_range[0], center_y), self)
        ur = Quadtree(self.mesh, self.bin_size, (center_x, self.x_range[1]), (center_y, self.y_range[1]), self)
        lr = Quadtree(self.mesh, self.bin_size, (center_x, self.x_range[1]), (self.y_range[0], center_y), self)
        ul = Quadtree(self.mesh, self.bin_size, (self.x_range[0], center_x), (center_y, self.y_range[1]), self)
        self._children = [ll, lr, ul, ur]

        # Move the data to the children
        while self._data:
            self.add_element(self._data.pop())

    def contains_element(self, element_number):

        n1, n2, n3 = self.mesh.element(element_number)
        return (self.contains_node(n1) or
                self.contains_node(n2) or
                self.contains_node(n3))

    def contains_node(self, node_number):

        return (self.x_range[0] <= self.mesh.node(node_number)[0] < self.x_range[1] and
                self.y_range[0] <= self.mesh.node(node_number)[1] < self.y_range[1])

    def contains_point(self, x, y):

        return (self.x_range[0] <= x < self.x_range[1] and
                self.y_range[0] <= y < self.y_range[1])