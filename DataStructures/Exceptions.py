class MeshError(Exception):
    """Basic exception for anything Mesh related"""

class DuplicateNodeNumberError( MeshError ):
    """When there is more than one node with the same node number"""
    def __init__( self, node_number ):
        self.node_number = node_number

class NodeDoesNotExistError( MeshError ):
    """When attempting to reference a node number that does not exist"""
    def __init__( self, node_number ):
        self.node_number = node_number

class DuplicateElementNumberError( MeshError ):
    """When there is more than one element with the same element number"""
    def __init__( self, element_number ):
        self.element_number = element_number