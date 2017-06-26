from DataStructures.Trees import Quadtree
from DataStructures.Items import Node, Element, MeshNode, MeshElement
from DataStructures.Shapes import PointShape
from Mesh import Mesh
import matplotlib.pyplot as plt

# Read the mesh
print( 'Reading mesh' )
mesh = Mesh( '/home/tristan/box/adcirc/runs/scaled20-noutgs/200' )
# mesh = Mesh( '/home/tristan/box/adcirc/runs/fran' )
mesh.read_fort14()

# Get the bounds
print( 'Bounding box: ', mesh.x_bounds, mesh.y_bounds )

# Build the quadtree
print( 'Building quadtree' )
q = Quadtree( mesh.x_bounds, mesh.y_bounds, 1000 )
for element_number, element in mesh.elements.items():

    e = MeshElement( mesh, element_number )
    q.add_item( e )

print( 'Performing a search' )
p = PointShape(
    (( mesh.x_bounds[0] + mesh.x_bounds[1] ) / 2.0) + 0.01,
    (( mesh.y_bounds[0] + mesh.y_bounds[1] ) / 2.0) + 0.01
)

elements = q.find(p)
print( elements )
xvals = [p.x]
yvals = [p.y]
cvals = [1]
for element in elements:
    nodes = element.mesh.elements[element.element_number]
    for node in nodes:
        xvals.append( element.mesh.nodes[node][0] )
        yvals.append( element.mesh.nodes[node][1] )
        cvals.append( 0 )

plt.scatter( xvals, yvals, c=cvals )
plt.show()

print( 'Done!' )