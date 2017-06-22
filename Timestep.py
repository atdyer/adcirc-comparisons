
class Timestep:

    def __init__( self ):

        self.fields = dict()
        self.min = dict()
        self.max = dict()

    def add_field( self, field ):

        self.fields[ field.name ] = field

    def nodal_value( self, field, node_number, *args ):

            if field in self.fields:

                return self.fields[ field ].value( node_number, args )

            else:

                print( '\tTimestep does not have field', field )

    def num_fields( self ):

        return len( self.fields )

    def data_range( self, field ):

        if field in self.fields:
            return self.fields[ field ].data_range()


class Field:

    def __init__( self, name, ndims, model_time, timestep ):

        self.name = name
        self.ndims = ndims
        self.model_time = model_time
        self.timestep = timestep
        self.data = dict()
        self.min = [ float( 'inf' ) ] * ndims
        self.max = [ -float( 'inf' ) ] * ndims

    def value( self, node_number, values=None ):

        if values is None:

            return self.data[ node_number ]

        if len( values ) != self.ndims:

            print( '\tUnable to set', self.name, ' value for node', node_number )
            print( '\tIncorrect number of dimensions' )
            return

        for i in range( self.ndims ):
            if values[i] != -99999 and values[i] < self.min[i]: self.min[i] = values[i]
            if values[i] != -99999 and values[i] > self.max[i]: self.max[i] = values[i]

        self.data[ node_number ] = values

    def data_range( self ):

        return [ self.min, self.max ]