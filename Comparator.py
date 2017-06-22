from Mesh import Mesh
from Shape import *
from math import sqrt

class Comparator:

    def __init__( self, base_mesh: Mesh, comp_mesh: Mesh, bounding_shape: Shape = InfiniteShape() ):

        self.meshes_compared = False
        self.elevations_compared = False
        self.velocities_compared = False

        self.base = base_mesh
        self.comp = comp_mesh
        self.bounds = bounding_shape

        self.common_nodes = dict()
        self.unique_nodes_base = dict()
        self.unique_nodes_comp = dict()

    def compare_elevation_timeseries( self ):

        # Make sure we've got common and unique nodes
        if not self.meshes_compared:
            self.compare_meshes()

        # Start at the beginning of the file
        self.base.start_fort63()
        self.comp.start_fort63()

        print( '\tComparing elevation timeseries data' )

        rmse_count = 0
        common_rmse = dict()
        for key in self.common_nodes.keys():
            common_rmse[ key ] = 0.0


        while self.base.has_next_elevation_timestep() and self.comp.has_next_elevation_timestep():

            base = self.base.next_timestep()
            comp = self.comp.next_timestep()

            if base.fields[ 'elevation' ].model_time == comp.fields[ 'elevation' ].model_time:

                print( '\tBase ', self.base.f63current, '/', self.base.f63ts, '\tComp ', self.comp.f63current, '/', self.comp.f63ts )

                base_elevations = base.fields[ 'elevation' ]
                comp_elevations = comp.fields[ 'elevation' ]

                for location, node_nums in self.common_nodes.items():
                    base_nn = node_nums[0]
                    comp_nn = node_nums[1]
                    base_ele = base_elevations.value( base_nn )[0]
                    comp_ele = comp_elevations.value( comp_nn )[0]
                    common_rmse[ location ] += ( base_ele - comp_ele ) ** 2

                rmse_count += 1

        for key, rmse in common_rmse.items():
            common_rmse[ key ] = sqrt( rmse / rmse_count )

        return common_rmse



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
        self.meshes_compared = True

        print( '\tCommon nodes:', len( self.common_nodes ) )
        print( '\t', self.base.dir )
        print( '\t\tUnique nodes:', len( self.unique_nodes_base ) )
        print( '\t', self.comp.dir )
        print( '\t\tUnique nodes:', len( self.unique_nodes_comp ) )