from Mesh import Mesh
from Comparator import Comparator

base = Mesh( '/home/tristan/box/adcirc/runs/scaled20-refinement/original' )
comp = Mesh( '/home/tristan/box/adcirc/runs/scaled20-refinement/10' )

comparator = Comparator( base, comp )
comparator.compare_meshes()