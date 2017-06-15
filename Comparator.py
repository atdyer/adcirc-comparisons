from Mesh import Mesh

class Comparator:

    def __init__( self, base_mesh: Mesh, comp_mesh: Mesh ):

        self.base = base_mesh
        self.comp = comp_mesh

        self.common_nodes = dict()
        self.uncommon_nodes = dict()

    def compare_meshes( self ):

        # Make sure both meshes have been read
        if not self.base.f14read:
            self.base.read_fort14()

        if not self.comp.f14read:
            self.comp.read_fort14()

        print( '\tComparing nodal locations' )

        # Count node occurences to determine which are unique and which overlap
        node_counts = dict()

        for nodes in [ self.base.nodes, self.comp.nodes ]:

            for node, ( x, y, d ) in nodes.items():

                key = ( x, y )
                if key not in node_counts:
                    node_counts[ key ] = []
                node_counts[ key ].append( node )

        print( len( node_counts ) )