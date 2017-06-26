from Mesh import Mesh
from Shape import Circle
from Comparator import Comparator

import matplotlib.pyplot as plt

base = Mesh( '/home/tristan/box/adcirc/runs/scaled20-noutgs/200' )
comp = Mesh( '/home/tristan/box/adcirc/runs/scaled20-noutgs/3200' )

circle = Circle( -77.9199990000, 33.8721240000, 0.05 )

comparator = Comparator( base, comp, circle )
comparator.compare_meshes()
rmse = comparator.compare_elevation_timeseries()

# with open( '/home/tristan/box/adcirc/runs/scaled20-noutgs/rmse.txt', 'w' ) as f:
#
#     for ( x, y ), e in rmse.items():
#
#         f.write( str( x ) + ',' + str( y ) + ',' + str( e ) + '\n' )

xvals = []
yvals = []
evals = []
for ( x, y ), e in rmse.items():

    xvals.append( x )
    yvals.append( y )
    evals.append( e )
    # print( x, y, e )

plt.scatter( xvals, yvals, c=evals )
plt.show()