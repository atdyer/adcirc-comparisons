from .Shapes import Shape, Infinite
from .Exceptions import *

class Mesh:

    def __init__(self):

        self._nodes = dict()
        self._elements = dict()
        self._mask = Infinite()
        
        self._x_bounds = None
        self._x_bounds_masked = None
        self._y_bounds = None
        self._y_bounds_masked = None
        self._z_bounds = None
        self._z_bounds_masked = None

    def add_node(self, node_number, x, y, z):

        if node_number in self._nodes: raise DuplicateNodeNumberError(node_number)
        self._nodes[node_number] = (x, y, z)
        self._expand_bounds(x, y, z)


    def add_element(self, element_number, n1, n2, n3):

        if element_number in self._elements: raise DuplicateElementNumberError(element_number)
        if n1 not in self._nodes: raise NodeDoesNotExistError(n1)
        if n2 not in self._nodes: raise NodeDoesNotExistError(n2)
        if n3 not in self._nodes: raise NodeDoesNotExistError(n3)
        self._elements[element_number] = (n1, n2, n3)

    def mask(self, shape: Shape):
        """Sets the mask used when generators are producing nodes or elements.

        Nodes will be produced by the generator if the fall into the given shape.
        Elements will be produced by the generator if all three of the nodes
        that comprise the element fall into the given shape.
        """

        self._mask = shape
        self._x_bounds_masked = None
        self._y_bounds_masked = None
        self._z_bounds_masked = None

    def node(self, node_number):
        """Returns the node, regardless of any masking that has been set"""

        return self._nodes[node_number] if node_number in self._nodes else None

    def nodes(self):
        """A generator that yields nodes that are not masked"""

        for node, (x, y, z) in self._nodes.items():

            if self._mask.contains_point(x, y):

                yield node, (x, y, z)

    def num_elements(self, masked=True):

        if not masked or type(self._mask) is Infinite:
            return len(self._elements)
        return sum(1 for _ in self.elements())

    def num_nodes(self, masked=True):

        if not masked or type(self._mask) is Infinite:
            return len(self._nodes)
        return sum(1 for _ in self.nodes())

    def element(self, element_number):
        """Returns the element, regardless of any masking that has been set"""

        return self._elements[element_number] if element_number in self._elements else None

    def elements(self):
        """A generator that yeilds elements that are not masked"""

        for element, nodes in self._elements.items():

            contained = True
            for node in nodes:
                x, y, _ = self._nodes[node]
                if not self._mask.contains_point(x, y):
                    contained = False
                    break
            if contained:
                yield element, nodes

    def read(self, fort14):
        """Reads nodes and elements from a fort.14 file"""

        if len(self._nodes) > 0 or len(self._elements) > 0:

            print('WARNING: Reading from file, existing mesh data will be deleted.')
            self._nodes = dict()
            self._elements = dict()

        with open( fort14, 'r' ) as f:

            # Skip the header
            f.readline()

            # Read info line
            dat = f.readline().split()
            num_elements = int(dat[0])
            num_nodes = int(dat[1])

            # Read nodes
            for n in range(num_nodes):

                dat = f.readline().split()
                nn = int(dat[0])
                x = float(dat[1])
                y = float(dat[2])
                d = float(dat[3])

                self.add_node(nn, x, y, d)

            # Read elements
            for e in range(num_elements):

                dat = f.readline().split()
                en = int(dat[0])
                n1 = int(dat[2])
                n2 = int(dat[3])
                n3 = int(dat[4])

                self.add_element(en, n1, n2, n3)

    def x_bounds(self, masked=True):

        if self._x_bounds is None:
            return [-float('inf'), float('inf')]
        else:
            if not masked or type(self._mask) is Infinite:
                return self._x_bounds
            else:
                if self._x_bounds_masked is None:
                    self._calculate_masked_bounds()
                return self._x_bounds_masked

    def y_bounds(self, masked=True):

        if self._y_bounds is None:
            return [-float('inf'), float('inf')]
        else:
            if not masked or type(self._mask) is Infinite:
                return self._y_bounds
            else:
                if self._y_bounds_masked is None:
                    self._calculate_masked_bounds()
                return self._y_bounds_masked

    def z_bounds(self, masked=True):

        if self._z_bounds is None:
            return [-float('inf'), float('inf')]
        else:
            if not masked or type(self._mask) is Infinite:
                return self._z_bounds
            else:
                if self._z_bounds_masked is None:
                    self._calculate_masked_bounds()
                return self._z_bounds_masked

    def _calculate_masked_bounds(self):

        for node, (x, y, z) in self.nodes():

            self._expand_masked_bounds(x, y, z)

    def _expand_bounds(self, x=None, y=None, z=None):

        if x is not None:
            if self._x_bounds is None: self._x_bounds = [float('inf'), -float('inf')]
            if x < self._x_bounds[0]: self._x_bounds[0] = x
            if x > self._x_bounds[1]: self._x_bounds[1] = x

        if y is not None:
            if self._y_bounds is None: self._y_bounds = [float('inf'), -float('inf')]
            if y < self._y_bounds[0]: self._y_bounds[0] = y
            if y > self._y_bounds[1]: self._y_bounds[1] = y

        if z is not None:
            if self._z_bounds is None: self._z_bounds = [float('inf'), -float('inf')]
            if z < self._z_bounds[0]: self._z_bounds[0] = z
            if z > self._z_bounds[1]: self._z_bounds[1] = z

        if type(self._mask) is not Infinite:
            self._expand_masked_bounds(x, y, z)
            
    def _expand_masked_bounds(self, x, y, z=None):
        
        if self._mask.contains_point(x, y):
            if self._x_bounds_masked is None: self._x_bounds_masked = [float('inf'), -float('inf')]
            if self._y_bounds_masked is None: self._y_bounds_masked = [float('inf'), -float('inf')]
            if x < self._x_bounds_masked[0]: self._x_bounds_masked[0] = x
            if x > self._x_bounds_masked[1]: self._x_bounds_masked[1] = x
            if y < self._y_bounds_masked[0]: self._y_bounds_masked[0] = y
            if y > self._y_bounds_masked[1]: self._y_bounds_masked[1] = y
            if z is not None:
                if self._z_bounds_masked is None:
                    self._z_bounds_masked = [float('inf'), -float('inf')]
                if z < self._z_bounds_masked[0]: self._z_bounds_masked[0] = z
                if z > self._z_bounds_masked[1]: self._z_bounds_masked[1] = z