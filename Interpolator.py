from DataStructures.Mesh import Mesh
from DataStructures.Quadtree import Quadtree
from DataStructures.Shapes import *

class Interpolator:

    def __init__(self, mask=None):

        print('Creating interpolator')

        self._meshes = []
        self._datasets = []
        self._quadtrees = []
        self._mask = mask if mask is not None else Infinite()

        self._nodes = dict()
        self._num_meshes = 0

        self._current_model_time = 0

    def add_mesh(self, mesh):

        print('Adding mesh to interpolator')
        print('\tNodes:', mesh.num_nodes(), '\tElements:', mesh.num_elements())

        # Apply the mask
        mesh.mask(self._mask)

        # Build the quadtree
        q = Quadtree(mesh, 5000)

        # Store the data
        self._meshes.append(mesh)
        self._quadtrees.append(q)
        self._num_meshes += 1

    def align(self):

        print('Aligning timesteps')

        if self._num_meshes < 1:

            print('ERROR: No meshes in Interpolator')
            return



    def flatten(self):

        print('Creating node set for interpolator')

        if self._num_meshes < 1:

            print('ERROR: No meshes in Interpolator')
            return

        # Build list of all nodes
        for i in range(self._num_meshes):

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

        print('\tNodes:', len(self._nodes))

        # Find the element that non-existant nodes fall into
        for coordinates, nodes in self._nodes.items():

            for i in range(self._num_meshes):

                if nodes[i] is None:

                    quadtree = self._quadtrees[i]
                    element = quadtree.find_element(coordinates[0], coordinates[1])

                    nodes[i] = -element if element is not None else None

    def next_timestep(self):

        pass