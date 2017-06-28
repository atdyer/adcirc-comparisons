from DataStructures.Mesh import Mesh
from DataStructures.Shapes import *
from Interpolator import Interpolator

mesh1 = Mesh()
mesh2 = Mesh()
mesh3 = Mesh()
mesh4 = Mesh()

mesh1.read('/home/tristan/box/adcirc/runs/scaled20-refinement/original/fort.14')
mesh2.read('/home/tristan/box/adcirc/runs/scaled20-refinement/1/fort.14')
mesh3.read('/home/tristan/box/adcirc/runs/scaled20-refinement/4/fort.14')
mesh4.read('/home/tristan/box/adcirc/runs/scaled20-refinement/10/fort.14')

# circle = Circle(-78.0094680, 33.8726840, 0.008)

interp = Interpolator()
interp.add_mesh(mesh3)
interp.add_mesh(mesh1)
interp.add_mesh(mesh2)
interp.add_mesh(mesh4)

interp.flatten()