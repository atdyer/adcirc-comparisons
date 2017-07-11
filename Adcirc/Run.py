from DataStructures.Mesh import Mesh
from DataStructures.Quadtree import Quadtree
from DataStructures.Shapes import Infinite
from .Files import Fort63, Fort64
import os.path

class Run:

    def __init__(self, directory, mask=Infinite()):

        domain_dir = directory.strip()
        if not domain_dir[-1] == '/':
            domain_dir += '/'

        self._dir = domain_dir
        self._mask = mask

        self.mesh = None
        self.quadtree = None
        self.elevation_timeseries = None
        self.velocity_timeseries = None

        print('Loading new ADCIRC run')

        if os.path.isfile(self._dir + 'fort.14'):

            print('\t\N{WHITE BULLET} Loading mesh (fort.14)...')
            self.mesh = Mesh(self._mask)
            self.mesh.read(self._dir + 'fort.14')
            print('\t\N{WHITE BULLET} Building quadtree...')
            self.quadtree = Quadtree(self.mesh, 5000)

        if os.path.isfile(self._dir + 'fort.63'):

            print('\t\N{WHITE BULLET} Loading elevation timeseries (fort.63)...')
            self.elevation_timeseries = Fort63(self._dir + 'fort.63')
            self.elevation_timeseries.apply_masked_mesh(self.mesh)

        if os.path.isfile(self._dir + 'fort.64'):

            print('\t\N{WHITE BULLET} Loading velocity timeseries (fort.64)...')
            self.velocity_timeseries = Fort64(self._dir + 'fort.64')
            self.velocity_timeseries.apply_masked_mesh(self.mesh)

    def next_elevation_timestep(self):

        if self.elevation_timeseries is not None:

            return self.elevation_timeseries.next_timestep()

        return None

    def next_velocity_timestepe(self):

        if self.velocity_timeseries is not None:

            return self.velocity_timeseries.next_timestep()

        return None