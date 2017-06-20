from Mesh import Mesh
from Shape import *

class Comparator:

    def __init__( self, base_mesh: Mesh, comp_mesh: Mesh, bounding_shape: Shape = InfiniteShape() ):

        self.base = base_mesh
        self.comp = comp_mesh
        self.bounds = bounding_shape

        self.common_nodes = dict()
        self.unique_nodes_base = dict()
        self.unique_nodes_comp = dict()

    def compare_meshes( self ):

        # Make sure both meshes have been read
        if not self.base.f14read:
            self.base.read_fort14()

        if not self.comp.f14read:
            self.comp.read_fort14()

        if isinstance( self.bounds, InfiniteShape ):
            print( '\tComparing nodal locations for entire domain' )
        else:
            print( '\tComparing nodal locations within shape:' )
            print( '\t\t', self.bounds )

        # Build dictionary of base mesh nodes
        base_nodes = dict()

        for node, ( x, y, d ) in self.base.nodes.items():

            n = ( x, y )
            if self.bounds.contains( n ):
                base_nodes[ n ] = node

        # Look for common nodes in the compare mesh
        for node, ( x, y, d ) in self.comp.nodes.items():

            key = ( x, y )
            if key in base_nodes:

                # The node is in both meshes, store the node numbers in the common nodes dictionary
                base_node_number = base_nodes[ key ]
                self.common_nodes[ key ] = [ base_node_number, node ]

                # Remove the common node from the base mesh nodes
                del base_nodes[ key ]

            else:

                if self.bounds.contains( key ):
                    self.unique_nodes_comp[ key ] = node

        self.unique_nodes_base = base_nodes

        print( '\tCommon nodes:', len( self.common_nodes ) )
        print( '\t', self.base.dir )
        print( '\t\tUnique nodes:', len( self.unique_nodes_base ) )
        print( '\t', self.comp.dir )
        print( '\t\tUnique nodes:', len( self.unique_nodes_comp ) )