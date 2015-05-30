from enum import Enum
from .utils import weighted_choice

BIOME_SIZE = 20


class Tile(Enum):
    GRASS_1 = 1
    GRASS_2 = 2
    DIRT_1 = 3


class Biome(object):
    def generate_biome(self):
        self.tiles = [[None]*BIOME_SIZE for _ in range(BIOME_SIZE)]

        for r in range(BIOME_SIZE):
            for c in range(BIOME_SIZE):
                self.tiles[r][c] = weighted_choice(self.tile_odds)

    def __str__(self):
        return '\n'.join(''.join(str(l.value) for l in row) for row in self.tiles)


class FieldBiome(Biome):

    tile_odds = {
        Tile.GRASS_1: 0.8,
        Tile.GRASS_2: 0.1,
        Tile.DIRT_1: 0.1,
    }
