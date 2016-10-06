import random
from enum import Enum
from .utils import weighted_choice
from .tiles import TileKind

BIOME_SIZE = 30


class Biome(object):
    def __init__(self):
        self.bombed = set()

    def initialize_base(self, tile):
        self.tiles = [[tile]*BIOME_SIZE for _ in range(BIOME_SIZE)]

    def generate_naive(self, tile_odds):
        """ generate a biome with a naive random approach """

        # create the tiles array w/ whatever
        self.initialize_base(None)

        for r in range(BIOME_SIZE):
            for c in range(BIOME_SIZE):
                self.tiles[r][c] = weighted_choice(tile_odds)

    def generate_seedbomb(self, tile, *, min, max, chance, attenuate):
        for _ in range(min):
            self.seedbomb(random.randrange(BIOME_SIZE), random.randrange(BIOME_SIZE),
                          tile, attenuate)
        bombs_hit = min
        while bombs_hit < max:
            if random.random() < chance:
                self.seedbomb(random.randrange(BIOME_SIZE), random.randrange(BIOME_SIZE),
                              tile, attenuate)
                bombs_hit += 1
            else:
                break

    def seedbomb(self, r, c, tile, attenuate):
        #if (0 <= r < BIOME_SIZE) and (0 <= c < BIOME_SIZE):
        self.tiles[r][c] = tile
        self.bombed.add((r, c))

        neighbors = ((r-1, c-1), (r-1, c), (r-1, c+1),
                     (r, c-1), (r, c+1),
                     (r+1, c-1), (r+1, c), (r+1, c)
                     )
        for nr, nc in neighbors:
            if ((0 <= nr < BIOME_SIZE) and (0 <= nc < BIOME_SIZE)
                and self.tiles[nr][nc] != tile and (nr, nc) not in self.bombed):
                # maybe also add bombed flag here?

                if random.random() < attenuate:
                    self.tiles[nr][nc] = tile

                    # square attenuate and propagate to neighbors
                    new_attenuate = attenuate ** 2
                    if new_attenuate > 0.05:
                        self.seedbomb(nr, nc, tile, new_attenuate)


    def __str__(self):
        return '\n'.join(''.join(str(l.value) for l in row) for row in self.tiles)


class FieldBiome(Biome):

    def generate(self):
        tile_odds = {
            TileKind.GRASS_1: 0.9,
            TileKind.GRASS_2: 0.1,
        }
        self.generate_naive(tile_odds)
        self.generate_seedbomb(TileKind.DIRT_1, min=2, max=10, chance=0.5, attenuate=0.5)
