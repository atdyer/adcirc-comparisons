
class FortND:

    def __init__(self, ndims, file):

        self.ndims = ndims

        try:
            self.f = open(file, 'r')
            self.header = self.f.readline()

            dat = self.f.readline().split()

            # The total number of available datasets
            self.num_datasets = int(dat[0])

            # The total number of nodes
            self.num_nodes = int(dat[1])

            # The number of timesteps at which data is written
            self.timestep_interval = int(dat[3])

            # The length of a timestep in seconds
            self.dt = float(dat[2])/self.timestep_interval

            # The next timestep that will be read when FordND.nodes() is called
            self._next_timestep = None

        except IOError:
            print('ERROR: Cannot open', file)
            exit()

    def next_timestep(self):

        if self.f:

            if self._next_timestep is None:

                dat = self.f.readline()
                time = float(dat[0])
                timestep = int(dat[1])
                self._next_timestep = time, timestep

            return self._next_timestep

    def nodes(self, node_set=None):

        if self.f:

            if self._next_timestep is None:

                print('ERROR: You must call FortND.next_timestep() before iterating through nodes')

            if node_set is None:

                for i in range(self.num_nodes):

                    yield self._read_next_node()

            else:

                for i in range(self.num_nodes):

                    node, values = self._read_next_node()

                    if node in node_set:

                        yield node, values

            self._next_timestep = None

    def _read_next_node(self):

        dat = self.f.readline().split()
        node = int(dat[0])
        values = []

        for i in range(self.ndims):
            values.append(float(dat[i+1]))

        return node,tuple(values)
