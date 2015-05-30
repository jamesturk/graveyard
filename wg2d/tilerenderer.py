from enum import Enum

class TileKind(Enum):
    GRASS = 1
    TREE = 2
    DIRT = 3
    SAND = 4


class Renderer(object):

    def __init__(self, window):
        self.window = window

    def draw(self, tiles):
        """ this draws all of the tiles to the screen """
