import pyglet
from .tiles import TileKind


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

        pixel_x_coord = 0
        pixel_y_coord = 0

        for row in tiles:
            for tile in row:
                (self.images[tile]).blit(pixel_x_coord, pixel_y_coord)
                pixel_x_coord += 16
            pixel_x_coord = 0
            pixel_y_coord += 16
