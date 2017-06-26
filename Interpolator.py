from Mesh import Mesh
from Timestep import Timestep

class Interpolator:

    def __init__( self ):

        self.meshes = []

        self.start_time = 0.0

    def add_mesh( self, mesh ):

        start_time = mesh