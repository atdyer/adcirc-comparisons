from Mesh import Mesh
from Shape import Circle
from Comparator import Comparator

import matplotlib.pyplot as plt

base = Mesh( '/home/tristan/box/adcirc/runs/scaled20-refinement/original' )
comp = Mesh( '/home/tristan/box/adcirc/runs/scaled20-refinement/10' )

circle = Circle( -77.9199990000, 33.8721240000, 0.01 )

comparator = Comparator( base, comp, circle )
comparator.compare_meshes()

common_nodes = comparator.common_nodes
xvals = []
yvals = []
for ( x, y ), node_numbers in common_nodes.items():

    xvals.append( x )
    yvals.append( y )

plt.scatter( xvals, yvals )
plt.show()