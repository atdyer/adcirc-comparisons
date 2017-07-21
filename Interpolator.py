import sys

class Interpolator:

    def __init__(self):

        print('Creating interpolator')

        self._meshes = []
        self._nodes = dict()
        self._timeseries = []

        self._initialized = False
        self._current_model_time = 0
        self._model_times = None

    def add_timeseries(self, timeseries):

        print('Adding timeseries to interpolator')

        self._timeseries.append(timeseries)
        self._meshes.append(timeseries.mesh())

        return len(self._timeseries) - 1

    def current_model_time(self):

        return self._current_model_time

    def timeseries_indices(self):

        return tuple(ts.dataset_index() for ts in self._timeseries)

    def advance(self):

        if not self._initialized:

            print('\t\N{WHITE BULLET} Advancing to first overlapping timestep...')

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
                while self._model_times[i][1] < self._current_model_time:

                    self._print_progress(self.timeseries_indices())

                    self._model_times[i] = self._timeseries[i].advance()

                    # Make sure there is data
                    if self._model_times[i] is None:
                        print('WARNING: The time ranges do not overlap for specified runs')
                        return None

            self._initialized = True

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

        print('Creating node set for interpolation')
        print('\t\N{WHITE BULLET} Determining minimum bounding box')
        
        x_bounds = [-float('inf'), float('inf')]
        y_bounds = [-float('inf'), float('inf')]
        
        for timeseries in self._timeseries:

            xb = timeseries.mesh().x_bounds()
            yb = timeseries.mesh().y_bounds()
            
            if xb[0] > x_bounds[0]: x_bounds[0] = xb[0]
            if xb[1] < x_bounds[1]: x_bounds[1] = xb[1]
            if yb[0] > y_bounds[0]: y_bounds[0] = yb[0]
            if yb[1] < y_bounds[1]: y_bounds[1] = yb[1]
            
        print('\t\N{WHITE BULLET} Building list of all nodes')

        for timeseries in self._timeseries:

            mesh = timeseries.mesh()

            for node_number, (x, y, z) in mesh.nodes():

                if self._is_inside(x, y, x_bounds, y_bounds):

                    key = (x, y)

                    if key not in self._nodes:

                        self._nodes[key] = [None]*len(self._timeseries)

        for i in range(len(self._timeseries)):

            mesh = self._timeseries[i].mesh()

            for node_number, (x, y, z) in mesh.nodes():

                key = (x, y)

                if key in self._nodes:

                    self._nodes[key][i] = node_number

        print('\t\N{WHITE BULLET} Finding elements for non-duplicate nodes')

        removal = set()
        for coordinates, nodes in self._nodes.items():

            for i in range(len(self._timeseries)):

                if nodes[i] is None:

                    quadtree = self._timeseries[i].mesh().quadtree()
                    element = quadtree.find_element(coordinates[0], coordinates[1])

                    if element is None:
                        removal.add(coordinates)
                    else:
                        nodes[i] = -element

        print('\t\N{WHITE BULLET} Removing nodes that do not overlap')
        for coordinates in removal:

            del self._nodes[coordinates]

        print('\t\N{WHITE BULLET} Nodes:', len(self._nodes))

    def nodes(self):

        return self._nodes.keys()

    def _value(self, node, timeseries, coordinates):

        if node > 0:

            return timeseries.nodal_value(node, self._current_model_time)

        else:

            return timeseries.elemental_value(abs(node), coordinates[0], coordinates[1], self._current_model_time)

    @staticmethod
    def _is_inside(x, y, x_bounds, y_bounds):

        return x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]

    @staticmethod
    def _print_progress(indices):

        string = ''

        for ts in indices:
            string += str(ts[0]) + '/' + str(ts[1]) + ', '

        sys.stdout.write('\t\N{WHITE BULLET} ' + string[:-2] + '\r')
        sys.stdout.flush()