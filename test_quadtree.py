# from DataStructures.Trees import Quadtree
# from DataStructures.Items import Node, Element, MeshNode, MeshElement
# from DataStructures.Shapes import PointShape
from DataStructures.Quadtree import Quadtree
from DataStructures.Mesh import Mesh
import matplotlib.pyplot as plt

# Read the mesh
print( 'Reading mesh' )
# mesh = Mesh( '/home/tristan/box/adcirc/runs/scaled20-noutgs/200' )
# mesh = Mesh( '/home/tristan/box/adcirc/runs/fran' )
# mesh.read_fort14()
mesh = Mesh()
mesh.read('/home/tristan/box/adcirc/runs/scaled20-noutgs/200/fort.14')

# Get the bounds
print( 'Bounding box: ', mesh.x_bounds(), mesh.y_bounds() )

# Build the quadtree
q = Quadtree(mesh, 1000)
print( 'Building the quadtree' )
q.add_elements()
print( 'Done!' )

# Perform a search
center_x = (mesh.x_bounds()[0] + mesh.x_bounds()[1]) / 2.0
center_y = (mesh.y_bounds()[0] + mesh.y_bounds()[1]) / 2.0
center_x += 0.001
e = q.find_element( center_x, center_y )
print( e )

# Draw the element and point
xvals = [center_x]
yvals = [center_y]
zvals = [0]

nodes = mesh.elements[e]
for node in nodes:
    xvals.append(mesh.nodes[node][0])
    yvals.append(mesh.nodes[node][1])
    zvals.append(1)

plt.scatter(xvals, yvals, c=zvals)
plt.show()