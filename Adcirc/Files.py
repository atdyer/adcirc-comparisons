from DataStructures.Timestep import Timestep

class File:

    def __init__(self, file):

        try:
            self.f = open(file, 'r')

        except IOError:
            print('Error: Cannot open', file)

class FortND(File):

    def __init__(self, ndims, file):

        super().__init__(file)
        self._ndims = ndims
        self._masked_mesh = None

        try:

            self.header = self.f.readline()

            dat = self.f.readline().split()

            # The total number of available datasets
            self.num_datasets = int(dat[0])

            # The total number of nodes
            self.num_nodes = int(dat[1])

            # The number of timesteps at which data is written
            self.timestep_interval = int(dat[3])

            # The length of a timestep in seconds
            self.dt = float(dat[2]) / self.timestep_interval

        except IOError:

            print('Error reading file', self.f)

    def apply_masked_mesh(self, mesh):

        self._masked_mesh = mesh

    def next_timestep(self):
        """Returns the next timestep in the file"""

        dat = self.f.readline().split()
        time = float(dat[0])
        iteration = int(dat[1])

        ts = Timestep(self._ndims, time, iteration)

        for i in range(self.num_nodes):

            dat = self.f.readline().split()
            node = int(dat[0])
            value = []

            if self._masked_mesh is None or self._masked_mesh.contains(node):

                for j in range(self._ndims):
                    value.append(float(dat[1+j]))

                ts.set(node, tuple(value))

        return ts

    def timesteps(self):
        """Iterator that yields all timesteps in the file"""

        for i in range(self.num_datasets):

            yield self.next_timestep()

class Fort63(FortND):

    def __init__(self, file):

        super().__init__(1, file)

class Fort64(FortND):

    def __init__(self, file):

        super().__init__(2, file)

class MaxFile(File):

    def __init__(self, file):

        # Open the file
        super().__init__(file)

        try:

            # Read header
            self.header = self.f.readline()

            dat = self.f.readline().split()

            # The total number of nodes
            self.num_nodes = int(dat[1])

            # The number of timesteps at which data is written
            self.timestep_interval = int(dat[3])

            # The length of a timestep in seconds
            self.dt = float(dat[2]) / self.timestep_interval

            # The number of data points per node
            self.ndims = int(dat[4])

            dat = self.f.readline().split()

            # The final model time
            self.final_time = float(dat[0])

            # The final model timestep
            self.final_timestep = int(dat[1])

            # The dictionary of nodes
            self.values = dict()
            self.times = dict()

            # Read the max values
            for i in range(self.num_nodes):

                dat = self.f.readline().split()

                # The node number
                nn = int(dat[0])

                # The value(s)
                val = tuple(dat[1:1+self.ndims])

                # Save the value(s) to the dictionary
                self.values[nn] = val

            dat = self.f.readline()

            if dat is not None:

                for i in range(self.num_nodes):

                    dat = self.f.readline().split()

                    # The node number
                    nn = int(dat[0])

                    # The time at which the maximum value occurred
                    time = float(dat[1])

                    # Save the time to the dictionary
                    self.times[nn] = time

        except IOError:
            print('Error reading file', self.f)

    def max_value(self, node):

        if node in self.values:

            return self.values[node]

        return None

    def max_time(self, node):

        if node in self.values:

            return self.times[node]

        return None

class MaxEle(MaxFile):
    """Extends MaxFile, which infers the number of dimensions automatically"""

class MaxVel(MaxFile):
    """Extends MaxFile, which infers the number of dimensions automatically"""

class MaxWVel(MaxFile):
    """Extends MaxFile, which infers the number of dimensions automatically"""

class MaxRS(MaxFile):
    """Extends MaxFile, which infers the number of dimensions automatically"""

class MinPR(MaxFile):
    """Extends MaxFile, which infers the number of dimensions automatically"""




