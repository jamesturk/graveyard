'''
    General utilities used throughout SRB
'''

from math import sqrt

def constrain(value, lbound, ubound):
    ''' Constrain value to be within range [lbound, ubount] '''
    return min(max(lbound, value), ubound)

def distance(p1, p2):
    # euclidean distance
    return sqrt( (p1.x-p2.x)**2 + (p1.y-p2.y)**2 )

class Point(object):
    __slots__ = ['x','y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, scalar):
        return Point(self.x*scalar, self.y*scalar)

    def __str__(self):
        return '(%f, %f)' % (self.x, self.y)
