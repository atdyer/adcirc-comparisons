from .Items import Point

class Quadtree:

    def __init__(self, x_range, y_range, bin_size, parent=None):

        # The data ranges
        self.x_range = x_range
        self.y_range = y_range
        self.edge_point = Point(x_range[0], y_range[0])

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

    def add_item(self, item):

        # Is this a branch?
        if self._children is not None:

            # Yes, so find the child it falls into
            for child in self._children:

                if item.is_inside( child ):

                    child.add_item( item )
                    return

        else:

            # No, so either add the item to this leaf or split this leaf into a branch
            if item.is_inside( self ):

                if len( self._data ) >= self.bin_size:

                    self._branch()
                    self.add_item(item)

                else:

                    self._data.append( item )

    def find(self, shape):

        _items = []

        # Check for an edge intersection
        if self._intersects(shape):

            # Check if this is a branch
            if self._children is not None:

                # It is, so recurse through children
                for child in self._children:

                    _child_items, _early_exit = child.find(shape)
                    _items = _items + _child_items

            else:

                # It isn't, so look through the data
                for item in self._data:

                    if shape.contains(item):

                        _items.append(item)

            return _items if self._depth == 0 else (_items, False)

        else:

            # There's no edge intersection, so if the shape's edge point
            # falls within this quad, we're done with the search after
            # recursing below this level
            if self._contains( shape.edge_point() ):

                # Check if this is a branch
                if self._children is not None:

                    # It is, so recurse through the children
                    for child in self._children:

                        # Get the search results from this child
                        _child_items, _early_exit = child.find(shape)
                        _items = _items + _child_items

                        # Check for early exit
                        if _early_exit:

                            return _items if self._depth == 0 else (_items, True)

                else:

                    # It isn't, so look through the data in this leaf
                    for item in self._data:

                        if shape.contains(item):

                            _items.append(item)

                # Perform an early exit
                return _items if self._depth == 0 else (_items, True)

            else:

                # There's no edge intersection and the shape doesn't fall
                # completely inside of a quad. Check to see if this quad
                # falls completely inside of the shape
                if shape.contains(self.edge_point):

                    _items += self._data

                return _items if self._depth == 0 else (_items, False)



    def depth(self):

        return self._depth

    def _branch(self):

        # Find the centerpoint
        center_x = (self.x_range[0] + self.x_range[1]) / 2.0
        center_y = (self.y_range[0] + self.y_range[1]) / 2.0

        # Create the children
        ll = Quadtree((self.x_range[0], center_x), (self.y_range[0], center_y), self.bin_size, self)
        ur = Quadtree((center_x, self.x_range[1]), (center_y, self.y_range[1]), self.bin_size, self)
        lr = Quadtree((center_x, self.x_range[1]), (self.y_range[0], center_y), self.bin_size, self)
        ul = Quadtree((self.x_range[0], center_x), (center_y, self.y_range[1]), self.bin_size, self)
        self._children = [ll, lr, ul, ur]

        # Move the data to the children
        while self._data:
            self.add_item( self._data.pop() )

    def _contains(self, point):

        return (self.x_range[0] <= point[0] < self.x_range[1] and
                self.y_range[0] <= point[1] < self.y_range[1])

    def _intersects(self, shape):

        return (shape.intersects(self.x_range[0], self.y_range[0], self.x_range[1], self.y_range[0]) or
                shape.intersects(self.x_range[0], self.y_range[0], self.x_range[0], self.y_range[1]) or
                shape.intersects(self.x_range[1], self.y_range[1], self.x_range[1], self.y_range[0]) or
                shape.intersects(self.x_range[1], self.y_range[1], self.x_range[0], self.y_range[1]))