class Timestep:

    def __init__(self, ndims, model_time, iteration, nan_val=-99999):

        self.model_time = model_time
        self.iteration = iteration

        self._nodes = dict()
        self._ndims = ndims
        self._min = [float('inf')] * ndims
        self._max = [-float('inf')] * ndims
        self._nan_val = nan_val

    def set(self, node, value):
        """Set the value at a node for this timestep"""

        # Add the value to the dictionary
        self._nodes[node] = value

        # Expand data range if necessary
        for i in range(self._ndims):

            if value[i] != self._nan_val:

                if value[i] < self._min[i]: self._min[i] = value[i]
                if value[i] > self._max[i]: self._max[i] = value[i]

    def get(self, node):
        """Get the value at a node for this timestep"""

        if node in self._nodes:

            return self._nodes[node]

        return None

    def nodes(self):
        """Iterator that yields all nodes in the timestep as a tuple containing (node, value)"""

        for node, value in self._nodes.items():

            yield node, value

    def range(self):
        """A tuple containing the min and max values of this timestep"""

        return tuple(self._min), tuple(self._max)
