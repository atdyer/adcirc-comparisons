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

        # Add the value to the dictionary
        self._nodes[node] = value

        # Expand data range if necessary
        for i in range(self._ndims):

            if value[i] != self._nan_val:

                if value[i] < self._min[i]: self._min[i] = value[i]
                if value[i] > self._max[i]: self._max[i] = value[i]

    def get(self, node):

        if node in self._nodes:

            return self._nodes[node]

        return None

    def nodes(self):

        for node in self._nodes:

            yield node

    def range(self):

        return tuple(self._min), tuple(self._max)
