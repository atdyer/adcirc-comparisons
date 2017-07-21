class Timestep:

    def __init__(self, ndims, model_time, iteration):

        self.model_time = model_time
        self.iteration = iteration

        self._nodes = dict()
        self._ndims = ndims

    def set(self, node, value):
        """Set the value at a node for this timestep"""

        # Add the value to the dictionary
        self._nodes[node] = value

    def get(self, node):
        """Get the value at a node for this timestep"""

        if node in self._nodes:

            return self._nodes[node]

        return None

    def nodes(self):
        """Iterator that yields all nodes in the timestep as a tuple containing (node, value)"""

        for node, value in self._nodes.items():

            yield node, value

