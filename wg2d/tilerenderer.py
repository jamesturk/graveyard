import pyglet
from .tiles import TileKind

TILE_SIZE = 16

class Renderer(object):

    def __init__(self, window):
        self.window = window
        self.images = {}
        self.images[TileKind.GRASS_1] = pyglet.image.load('./images/grass1.png')
        self.images[TileKind.GRASS_2] = pyglet.image.load('./images/grass2.png')
        self.images[TileKind.WATER_1] = pyglet.image.load('./images/blue.jpg')
        self.images[TileKind.DIRT_1] = pyglet.image.load('./images/dirt1.png')


    def draw(self, tiles):
        """ this draws all of the tiles to the screen """

        for pos, tile in tiles:
            self.images[tile].blit(pos.x*TILE_SIZE, pos.y*TILE_SIZE)
