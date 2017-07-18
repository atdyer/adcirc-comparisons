from DataStructures.Mesh import Mesh
from DataStructures.Shapes import Infinite
from DataStructures.Timeseries import Timeseries
import os.path

class Run:

    def __init__(self, directory, mask=Infinite()):

        domain_dir = directory.strip()
        if not domain_dir[-1] == '/':
            domain_dir += '/'

        self._dir = domain_dir
        self._mask = mask

        self.mesh = None
        self.elevation_timeseries = None
        self.velocity_timeseries = None

        print('Loading new ADCIRC run')

        if os.path.isfile(self._dir + 'fort.14'):

            print('\t\N{WHITE BULLET} Loading mesh (fort.14)...')
            self.mesh = Mesh(self._mask)
            self.mesh.read(self._dir + 'fort.14')
            self.mesh.quadtree()

        if os.path.isfile(self._dir + 'fort.63'):

            print('\t\N{WHITE BULLET} Loading elevation timeseries (fort.63)...')
            self.elevation_timeseries = Timeseries(1, self._dir + 'fort.63', self.mesh)

        if os.path.isfile(self._dir + 'fort.64'):

            print('\t\N{WHITE BULLET} Loading velocity timeseries (fort.64)...')
            self.velocity_timeseries = Timeseries(2, self._dir + 'fort.64', self.mesh)