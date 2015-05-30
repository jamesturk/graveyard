from enum import Enum
import pyglet

class TileKind(Enum):
    GRASS = 1
    WATER = 2
    DIRT = 3
    SAND = 4


class Renderer(object):

    def __init__(self, window):
        self.window = window
        self.images = {}
        self.images[TileKind.GRASS.value] = pyglet.image.load('./wg2d/images/green.jpg')
        self.images[TileKind.WATER.value] = pyglet.image.load('./wg2d/images/blue.jpg')
        self.images[TileKind.DIRT.value] = pyglet.image.load('./wg2d/images/brown.jpg')
        self.images[TileKind.SAND.value] = pyglet.image.load('./wg2d/images/yellow.jpg')



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
