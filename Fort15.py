
class Fort15:

    def __init__( self, file=None ):

        self.RUNDES = None
        self.RUNID = None
        self.NFOVER = None
        self.NABOUT = None
        self.NSCREEN = None
        self.IHOT = None
        self.ICS = None
        self.IM = None
        self.IDEN = None
        self.NOLIBF = None
        self.NOLIFA = None
        self.NOLICA = None
        self.NOLICAT = None
        self.NWP = None
        self.nodal_attributes = None
        self.NCOR = None
        self.NTIP = None
        self.NWS = None
        self.NRAMP = None
        self.G = None
        self.TAU0 = None
        self.Tau0FullDomainMin = None
        self.Tau0FullDomainMax = None
        self.DTDP = None
        self.STATIM = None
        self.REFTIM = None
        self.RNDAY = None

        if file is not None:

            self.read_file( file )

    def read_file( self, file ):

        with open( file, 'r' ) as f:

            self.RUNDES = self.__read_line( f )
            self.RUNID = self.__read_line( f )
            self.NFOVER = int( self.__read_line( f ) )
            self.NABOUT = int( self.__read_line( f ) )
            self.NSCREEN = int( self.__read_line( f ) )
            self.IHOT = int( self.__read_line( f ) )
            self.ICS = int( self.__read_line( f ) )
            self.IM = int( self.__read_line( f ) )
            if self.IM == 20:
                self.IDEN = int( self.__read_line( f ) )
            self.NOLIBF = int( self.__read_line( f ) )
            self.NOLIFA = int( self.__read_line( f ) )
            self.NOLICA = int( self.__read_line( f ) )
            self.NOLICAT = int( self.__read_line( f ) )
            self.NWP = int( self.__read_line( f ) )
            if self.NWP > 0:
                self.nodal_attributes = []
                for i in range( self.NWP ):
                    self.nodal_attributes.append( self.__read_line( f ) )
            self.NCOR = int( self.__read_line( f ) )
            self.NTIP = int( self.__read_line( f ) )
            self.NWS = int( self.__read_line( f ) )
            self.NRAMP = int( self.__read_line( f ) )
            self.G = float( self.__read_line( f ) )
            self.TAU0 = float( self.__read_line( f ) )
            if self.TAU0 == -5:
                dat = self.__read_line( f ).split()
                self.Tau0FullDomainMin = float( dat[0] )
                self.Tau0FullDomainMax = float( dat[1] )
            self.DTDP = float( self.__read_line( f ) )
            self.STATIM = float( self.__read_line( f ) )
            self.REFTIM = float( self.__read_line( f ) )

    @staticmethod
    def __read_line( f ):

        return f.readline().split('!')[0]
