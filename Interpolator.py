from DataStructures.Mesh import Mesh
from DataStructures.Quadtree import Quadtree
from DataStructures.Shapes import *

class Interpolator:

    def __init__(self):

        print('Creating interpolator')

        self._meshes = []
        self._nodes = dict()
        self._timeseries = []

        self._initialized = False
        self._current_model_time = 0
        self._model_times = None

        self._ts1 = []
        self._ts2 = []
        self._elevation_indices = []

    def add_timeseries(self, timeseries):

        print('Adding timeseries to interpolator')

        self._timeseries.append(timeseries)
        self._meshes.append(timeseries.mesh())

    def advance(self):

        if not self._initialized:

            self._model_times = [timeseries.advance() for timeseries in self._timeseries]

            if None in self._model_times:
                return None

            # The first possible timestep will be the one that starts the latest
            self._current_model_time = -float('inf')
            for time_range in self._model_times:
                if time_range[1] > self._current_model_time:
                    self._current_model_time = time_range[1]

            # Now make sure that each timeseries is overlapping the latest time
            for i in range(len(self._model_times)):

                # The the end time comes before the target time, we need to advance
                if self._model_times[i][1] < self._current_model_time:

                    self._model_times[i] = self._timeseries[i].advance()

                    # Make sure there is data
                    if self._model_times[i] is None:
                        return None

            return self._current_model_time

        else:

            # Advance any timestep whose second ts falls on the current ts
            for i in range(len(self._model_times)):

                if self._current_model_time == self._model_times[i][1]:

                    self._model_times[i] = self._timeseries[i].advance()

                    # Check that there's data
                    if self._model_times[i] is None:

                        return None

            next_model_time = float('inf')

            # Determine the next model time to use
            for i in range(len(self._model_times)):

                if self._current_model_time < self._model_times[i][1] < next_model_time:

                    next_model_time = self._model_times[i][1]

            self._current_model_time = next_model_time

            return self._current_model_time

    def current_timestep(self):

        for coordinates, nodes in self._nodes.items():

            yield coordinates, tuple(self._value(node, ts, coordinates) for node, ts in zip(nodes, self._timeseries))


    def flatten(self):
        """Determines all nodes that will be used to provide data"""

        print('Creating node set for interpolator')

        # Build list of all nodes
        for i in range(len(self._meshes)):

            mesh = self._meshes[i]

            # Every node in the dictionary will have a list with a value
            # for each mesh. The value will be a node number if that node
            # exists in the mesh, and will be None if it does not
            for node_number, (x, y, z) in mesh.nodes():

                key = (x, y)

                if key not in self._nodes:

                    self._nodes[key] = [None]*(i-1)

                while len(self._nodes[key]) < i:

                    self._nodes[key].append(None)

                self._nodes[key].append(node_number)

        # Fill in the last slot(s)
        for key in self._nodes.keys():

            while len(self._nodes[key]) < len(self._meshes):

                self._nodes[key].append(None)

        print('\t\N{WHITE BULLET} Nodes:', len(self._nodes))

        # Find the element that non-existant nodes fall into
        for coordinates, nodes in self._nodes.items():

            for i in range(len(self._meshes)):

                if nodes[i] is None:

                    quadtree = self._meshes[i].quadtree()
                    element = quadtree.find_element(coordinates[0], coordinates[1])

                    nodes[i] = -element if element is not None else None

    def _value(self, node, timeseries, coordinates):

        if node > 0:

            return timeseries.nodal_value(node, self._current_model_time)

        else:

            return timeseries.elemental_value(abs(node), coordinates[0], coordinates[1], self._current_model_time)