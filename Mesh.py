import os
from MeshExceptions import *

class Mesh:

    def __init__( self, domain_dir ):

        domain_dir = domain_dir.strip()
        if not domain_dir[-1] == '/':
            domain_dir += '/'

        self.dir = domain_dir

        # File statuses
        self.f14read = False
        self.f63read = False
        self.f64read = False

        # Mesh properties
        self.f14header = None
        self.num_nodes = None
        self.num_elements = None
        self.nodes = None
        self.elements = None
        self.x_bounds = None
        self.y_bounds = None

        # Mesh boundaries
        self.elev_boundary_segments = None
        self.elev_boundary_nodes = None
        self.flow_boundary_segments = None
        self.flow_boundary_nodes = None
        self.num_elev_boundary_segments = None
        self.num_elev_boundary_nodes = None
        self.num_flow_boundary_segments = None
        self.num_flow_boundary_nodes = None


    # Returns True if the domain has been run
    def is_completed_run( self ):

        return os.path.exists( self.dir + 'fort.63' ) and os.path.exists( self.dir + 'fort.64' )


    # Opens and returns an input file with a given name at the domain's directory
    def open_input_file( self, filename ):

        try:
            f = open( self.dir + filename )
            return f
        except IOError:
            print( 'Error: Cannot open', filename, 'at', self.dir )
            exit()


    # Opens elevation timeseries file for reading
    def read_fort63( self ):

        if not os.path.exists( self.dir + 'fort.63' ):
            print( '\tRun not completed, unable to read elevation timeseries.' )
            return

        print( '\tReading fort.63 at', self.dir )

    # Opens velocity timeseries file for reading
    def read_fort64( self ):

        print( '\tReading fort.64 at', self.dir )

    # Reads the mesh
    def read_fort14( self ):

        print( '\tReading fort.14 at', self.dir )
        f = self.open_input_file( 'fort.14' )

        # Read the header
        self.f14header = f.readline()

        # Read number of nodes and elements
        l = f.readline().split()
        self.num_elements = int( l[0] )
        self.num_nodes = int( l[1] )

        # Initialize the dictionaries for nodes and elements
        self.nodes = dict()
        self.elements = dict()

        try:

            self.x_bounds = [ float( 'inf' ), -float( 'inf' ) ]
            self.y_bounds = [ float( 'inf' ), -float( 'inf' ) ]

            # Read the nodes
            for n in range( self.num_nodes ):

                dat = f.readline().split()
                node_number = int( dat[0] )
                x = float( dat[1] )
                y = float( dat[2] )
                d = float( dat[3] )

                # Check that the node number is not a duplicate
                if node_number not in self.nodes:

                    self.nodes[ node_number ] = ( x, y, d )

                    if x < self.x_bounds[0]: self.x_bounds[0] = x
                    if x > self.x_bounds[1]: self.x_bounds[1] = x
                    if y < self.y_bounds[0]: self.y_bounds[0] = y
                    if y > self.y_bounds[1]: self.y_bounds[1] = y

                else:

                    raise DuplicateNodeNumberError( node_number )

            # Read the elements
            for e in range( self.num_elements ):

                dat = f.readline().split()
                ele_number = int( dat[0] )
                n1 = int( dat[2] )
                n2 = int( dat[3] )
                n3 = int( dat[4] )

                # Check that node numbers are in the node list
                if n1 not in self.nodes: raise NodeDoesNotExistError( n1 )
                if n2 not in self.nodes: raise NodeDoesNotExistError( n2 )
                if n3 not in self.nodes: raise NodeDoesNotExistError( n3 )

                # Check that the element number is not a duplicate
                if ele_number not in self.elements:

                    self.elements[ ele_number ] = ( n1, n2, n3 )

                else:

                    raise DuplicateElementNumberError( ele_number )

            # Read boundary information
            dat = f.readline().split()
            self.num_elev_boundary_segments = int( dat[0] )
            dat = f.readline().split()
            self.num_elev_boundary_nodes = int( dat[0] )
            self.elev_boundary_segments = []
            self.elev_boundary_nodes = set()

            for s in range( self.num_elev_boundary_segments ):

                dat = f.readline().split()

                # Get the number of nodes in this segment
                num_nodes = int( dat[0] )
                segment = []

                for n in range( num_nodes ):

                    # Read the next node number
                    dat = f.readline().split()
                    node = int( dat[0] )

                    # Make sure the node exists
                    if node not in self.nodes:
                        raise NodeDoesNotExistError( node )

                    # Add the node to the segment and the set of elevation boundary nodes
                    segment.append( node )
                    self.elev_boundary_nodes.add( node )

                # Add the segment to the list of segments
                self.elev_boundary_segments.append( segment )

            dat = f.readline().split()
            self.num_flow_boundary_segments = int( dat[0] )
            dat = f.readline().split()
            self.num_flow_boundary_nodes = int( dat[0] )
            self.flow_boundary_segments = []
            self.flow_boundary_nodes = set()

            for s in range( self.num_flow_boundary_segments ):

                dat = f.readline().split()

                # Get the number of nodes in this segment
                num_nodes = int( dat[0] )
                segment = []

                for n in range( num_nodes ):

                    # Read the next node number
                    dat = f.readline().split()
                    node = int( dat[0] )

                    # Make sure the node exists
                    if node not in self.nodes:
                        raise NodeDoesNotExistError( node )

                    # Add the node to the segment and the set of flow boundary nodes
                    segment.append( node )
                    self.flow_boundary_nodes.add( node )

                # Add the segment to the list of segments
                self.flow_boundary_segments.append( segment )


        except DuplicateNodeNumberError as err:

            print( 'Duplicate node number found in', self.dir )
            print( '\tNode number:', err.node_number )
            f.close()
            exit()

        except NodeDoesNotExistError as err:


            print( 'Unable to resolve node number in', self.dir )
            print( '\tNode number:', err.node_number )
            f.close()
            exit()

        except DuplicateElementNumberError as err:

            print( 'Duplicate element number found in ', self.dir )
            print( '\tElement number:', err.element_number )
            f.close()
            exit()

        finally:

            f.close()
            self.f14read = True


    def print_mesh_info(self):

        print( '\t', self.f14header.strip() )
        print( '\tNodes:', self.num_nodes )
        print( '\tElements:', self.num_elements )
        print( '\tElevation specified boundary nodes:', self.num_elev_boundary_nodes, '(', len( self.elev_boundary_nodes ), ')' )
        print( '\tElevation specified boundary segments:', self.num_elev_boundary_segments, '(', len( self.elev_boundary_segments ), ')' )
        print( '\tFlow specified boundary nodes:', self.num_flow_boundary_nodes, '(', len( self.flow_boundary_nodes ), ')' )
        print( '\tFlow specified boundary segments:', self.num_flow_boundary_segments, '(', len( self.flow_boundary_segments ), ')' )