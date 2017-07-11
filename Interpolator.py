from DataStructures.Mesh import Mesh
from DataStructures.Quadtree import Quadtree
from DataStructures.Shapes import *

class Interpolator:

    def __init__(self):

        print('Creating interpolator')

        self._runs = []
        self._nodes = dict()
        self._current_model_time = 0

        self._ts1 = []
        self._ts2 = []
        self._elevation_indices = []

    def add_run(self, run):

        print('Adding ADCIRC run to interpolator')

        # Store the run
        self._runs.append(run)

    def _advance(self):

        return True

    @staticmethod
    def _interpolate_value(start_ts, end_ts, node, time):

        if time == start_ts.model_time: return start_ts.get(node)
        if time == end_ts.model_time: return end_ts.get(node)
        if start_ts.model_time < time < end_ts.model_time:
            percent = (time - start_ts.model_time) / (end_ts.model_time - start_ts.model_time)
            start_vals = start_ts.get(node)
            end_vals = end_ts.get(node)
            # if node == 17132:
                # print(percent, start_vals, end_vals)
            return tuple( s + percent * (f-s) for s in start_vals for f in end_vals)
        return None

    def _elevations(self, time):

        for coordinates, node_list in self._nodes.items():

            for i in self._elevation_indices:

                node_number = node_list[i]
                start = self._ts1[i]
                finish = self._ts2[i]

                if node_number > 0:

                    yield i, node_number, self._interpolate_value(start, finish, node_number, time)


    def align_elevation_timeseries(self):
        """Determines the first timestep at which data will be generated"""

        print('Aligning timesteps')

        num_runs = len(self._runs)

        # Empty out the first and second timesteps
        self._ts1 = [None] * num_runs
        self._ts2 = [None] * num_runs

        # Get indices of runs that have elevation timeseries
        indices = []
        for i in range(num_runs):
            if self._runs[i].elevation_timeseries is not None:
                indices.append(i)

        # Load first and second timesteps
        for i in indices:

            self._ts1[i] = self._runs[i].next_elevation_timestep()
            self._ts2[i] = self._runs[i].next_elevation_timestep()

        # The first possible timestep will the the one that starts the latest
        latest_ts = -float('inf')
        for i in indices:

            if self._ts1[i].model_time > latest_ts:

                latest_ts = self._ts1[i].model_time

        # Now ensure that each run is at an overlapping point in time
        for i in indices:

            while self._ts2[i].model_time < latest_ts:

                self._ts1[i] = self._ts2[i]
                self._ts2[i] = self._runs[i].next_elevation_timestep()

        self._elevation_indices = indices

    def calculate_maximum_elevation_differences(self):

        times = [1800, 2700, 3600]

        for t in times:

            for i, node, val in self._elevations(t):

                if node == 17132 and i == 0:
                    print(t, '% 4.10f' % val[0])


    def flatten(self):
        """Determines all nodes that will be used to provide data"""

        print('Creating node set for interpolator')

        # Build list of all nodes
        for i in range(len(self._runs)):

            mesh = self._runs[i].mesh

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

            while len(self._nodes[key]) < len(self._runs):

                self._nodes[key].append(None)

        print('\t\N{WHITE BULLET} Nodes:', len(self._nodes))

        # Find the element that non-existant nodes fall into
        for coordinates, nodes in self._nodes.items():

            for i in range(len(self._runs)):

                if nodes[i] is None:

                    quadtree = self._runs[i].quadtree
                    element = quadtree.find_element(coordinates[0], coordinates[1])

                    nodes[i] = -element if element is not None else None