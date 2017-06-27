from DataStructures.Mesh import Mesh
from DataStructures.Shapes import Circle
from DataStructures.Quadtree import Quadtree

# Read the mesh from file
mesh = Mesh()
# mesh.read('/home/tristan/box/adcirc/runs/scaled20-noutgs/200/fort.14')
mesh.read('/home/tristan/box/adcirc/runs/fran/fort.14')
print('x-bounds:', mesh.x_bounds())
print('y-bounds:', mesh.y_bounds())

# Print the number of nodes and elements
num_nodes = sum(1 for _ in mesh.nodes())
num_elements = sum(1 for _ in mesh.elements())

print('Nodes:', num_nodes)
print('Elements:', num_elements)

# Create a circle and mask the mesh
center_x = (mesh.x_bounds()[0] + mesh.x_bounds()[1]) / 2.0
center_y = (mesh.y_bounds()[0] + mesh.y_bounds()[1]) / 2.0
circle = Circle(center_x, center_y, 1.0)
mesh.mask(circle)

# Print the number of nodes and elements
num_nodes = sum(1 for _ in mesh.nodes())
num_elements = sum(1 for _ in mesh.elements())

print('x-bounds:', mesh.x_bounds())
print('y-bounds:', mesh.y_bounds())
print('Nodes:', num_nodes)
print('Elements:', num_elements)

# Create a quadtree from the masked mesh
quadtree = Quadtree(mesh, 1000)
print('Quadtree depth:', quadtree.max_depth())

# Perform a search
center_x = (mesh.x_bounds()[0] + mesh.x_bounds()[1]) / 2.0
center_y = (mesh.y_bounds()[0] + mesh.y_bounds()[1]) / 2.0
element = quadtree.find_element(center_x, center_y)
print('Found element:', element)