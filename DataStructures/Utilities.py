def point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):

    AB = ( x2-x1, y2-y1 )
    BC = ( x3-x2, y3-y2 )
    CA = ( x1-x3, y1-y3 )

    AP = ( x-x1, y-y1 )
    BP = ( x-x2, y-y2 )
    CP = ( x-x3, y-y3 )

    A = cross(AB, AP)
    B = cross(BC, BP)
    C = cross(CA, CP)

    return (A>=0 and B>=0 and C>=0) or (A<0 and B<0 and C<0)

def cross(A, B):

    return A[0]*B[1] - A[1]*B[0]