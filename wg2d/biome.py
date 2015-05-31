import random
from enum import Enum
from .utils import weighted_choice
from .tiles import TileKind

BIOME_SIZE = 30


class Biome(object):
    def generate_naive(self, tile_odds):
        """ generate a biome with a naive random approach """
        self.tiles = [[None]*BIOME_SIZE for _ in range(BIOME_SIZE)]

        for r in range(BIOME_SIZE):
            for c in range(BIOME_SIZE):
                self.tiles[r][c] = weighted_choice(self.tile_odds)

    def generate_seedbomb(self, base_tile, seedbomb_rules):
        self.tiles = [[base_tile]*BIOME_SIZE for _ in range(BIOME_SIZE)]
        self.bombed = [[False]*BIOME_SIZE for _ in range(BIOME_SIZE)]

        for tile, rules in seedbomb_rules.items():
            for _ in range(rules['min']):
                self.seedbomb(random.randrange(BIOME_SIZE), random.randrange(BIOME_SIZE),
                              tile, rules['attenuate'])
            bombs_hit = rules['min']
            while bombs_hit < rules['max']:
                if random.random() < rules['chance']:
                    self.seedbomb(random.randrange(BIOME_SIZE), random.randrange(BIOME_SIZE),
                                  tile, rules['attenuate'])
                    bombs_hit += 1
                else:
                    break

    def seedbomb(self, r, c, tile, attenuate):
        if (0 <= r < BIOME_SIZE) and (0 <= c < BIOME_SIZE):
            self.tiles[r][c] = tile

            neighbors = ((r-1, c-1), (r-1, c), (r-1, c+1),
                         (r, c-1), (r, c+1),
                         (r+1, c-1), (r+1, c), (r+1, c)
                         )
            for nr, nc in neighbors:
                if ((0 <= nr < BIOME_SIZE) and (0 <= nc < BIOME_SIZE)
                    and self.tiles[nr][nc] != tile):
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

    def generate_naive(self):
        tile_odds = {
            TileKind.GRASS_1: 0.8,
            TileKind.GRASS_2: 0.1,
            TileKind.DIRT_1: 0.1,
        }
        super().generate_naive(tile_odds)

    def generate_seedbomb(self):
        rules = {
            TileKind.GRASS_2: {'min': 2, 'max': 10, 'chance': 0.7, 'attenuate': 0.6},
            TileKind.DIRT_1: {'min': 1, 'max': 10, 'chance': 0.5, 'attenuate': 0.3},
        }
        super().generate_seedbomb(TileKind.GRASS_1, rules)
