from Adcirc.Files import FortND
from DataStructures.Utilities import cross

class Timeseries:

    def __init__(self, ndims, fortnd, mesh=None):

        self._mesh = mesh
        self._fortnd = FortND(ndims, fortnd)

        if self._mesh is not None:
            self._fortnd.apply_masked_mesh(self._mesh)

        self._ts1 = None
        self._ts2 = None

    def advance(self):

        if self._ts1 is None and self._ts2 is None:

            return self._initialize()

        self._ts1 = self._ts2
        self._ts2 = self._fortnd.next_timestep()

        if self._ts2 is None:

            return None

        return self._ts1.model_time, self._ts2.model_time

    def dimensions(self):

        return self._fortnd.num_dimensions()

    def mesh(self):

        return self._mesh

    def nodal_value(self, node, model_time):
        """Returns the value at a node, interpolating in time if necessary"""

        if model_time == self._ts1.model_time:

            # print('No time interpolation:', self._ts1.get(node))
            return self._ts1.get(node)

        if model_time == self._ts2.model_time:

            # print('No time interpolation:', self._ts2.get(node))
            return self._ts2.get(node)

        if self._ts1.model_time < model_time < self._ts2.model_time:

            t1 = self._ts1.model_time
            v1 = self._ts1.get(node)
            t2 = self._ts2.model_time
            v2 = self._ts2.get(node)

            dat = tuple(self._linear_interpolate(t1, t2, a, b, model_time) for a in v1 for b in v2)
            # print('Time interpolate:', dat)

            return dat

    def elemental_value(self, element, x, y, model_time):
        """Returns an interplated value for a point inside of an element, interpolating in time if necessary"""

        nodes = self._mesh.element(element)
        n1 = self._mesh.node(nodes[0])
        n2 = self._mesh.node(nodes[1])
        n3 = self._mesh.node(nodes[2])

        f1 = (n1[0]-x, n1[1]-y)
        f2 = (n2[0]-x, n2[1]-y)
        f3 = (n3[0]-x, n3[1]-y)

        a = cross((n1[0]-n2[0], n1[1]-n2[1]), (n1[0]-n3[0], n1[1]-n3[1]))
        a1 = cross(f2, f3) / a
        a2 = cross(f3, f1) / a
        a3 = cross(f1, f2) / a

        v1 = self.nodal_value(nodes[0], model_time)
        v2 = self.nodal_value(nodes[1], model_time)
        v3 = self.nodal_value(nodes[2], model_time)

        return tuple(a1*_v1 + a2*_v2 + a3*_v3 for _v1, _v2, _v3 in zip(v1, v2, v3))

    def _initialize(self):

        self._ts1 = self._fortnd.next_timestep()
        self._ts2 = self._fortnd.next_timestep()

        return self._ts1.model_time, self._ts2.model_time

    @staticmethod
    def _linear_interpolate(t1, t2, x1, x2, t):

        p = (t - t1) / (t2 - t1)
        return x1 + p * (x2 - x1)