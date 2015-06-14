from collections import namedtuple

P = namedtuple('Point', ['x', 'y'])


class World(object):

    def __init__(self):
        # Point : TileKind
        self.tiles = {}

    def get_tiles(self, origin, width, height):
        for x in range(origin.x, origin.x + width):
            for y in range(origin.y, origin.y + height):
                p = P(x, y)
                yield p, self.tiles[p]

    def adopt_biome(self, biome, offset_x=0, offset_y=0):
        for x in range(len(biome.tiles)):
            for y in range(len(biome.tiles)):
                self.tiles[P(x+offset_x, y+offset_y)] = biome.tiles[x][y]
