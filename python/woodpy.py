from enum import Enum

DEFAULT_LUMBER_LENGTH = 8*12

class Dimension(Enum):
    HEIGHT = "height"
    WIDTH = "width"
    LENGTH = "length"


class Lumber:
    def __init__(self, height, width, length=DEFAULT_LUMBER_LENGTH):
        self.height = height
        self.width = width
        self.length = length

    def crosscut(self, length, times=1):
        result = ([Lumber(self.height, self.width, length) for n in range(times)] +
                [Lumber(self.height, self.width, self.length - length * times)])
        print(f"crosscut {times}x {length} pieces from {self} -> {result}")
        return result

    def rip(self, width):
        result = [Lumber(self.height, width, self.length), Lumber(self.height, self.width - width, self.length)]
        print(f"rip {self} at {width} -> {result}")
        return result

    def __repr__(self):
        return f"{self.height}x{self.width}x{self.length}"


def glue(pieces: list[Lumber], along: Dimension):
    height = pieces[0].height
    width = pieces[0].width
    length = pieces[0].length
    for p in pieces[1:]:
        if p.height != height:
            height = False
        if p.width != width:
            width = False
        if p.length != length:
            length = False
    assert height and length and length # too strict
    if along == Dimension.WIDTH:
        new = Lumber(height, width * len(pieces), length)
    elif along == Dimension.HEIGHT:
        new = Lumber(height * len(pieces), width, length)
    elif along == Dimension.LENGTH:
        new = Lumber(height, width, length * len(pieces))
    print(f"glue {pieces} along {along} -> {new}")
    return new

TwoByFour = Lumber(1.5, 3.5)

*pieces, board = TwoByFour.crosscut(7.5, 3)
base = glue(pieces, Dimension.WIDTH)
base, junk = base.rip(7.5)

*pieces, board = board.crosscut(5, 2)
tier2 = glue(pieces, Dimension.WIDTH)
tier2, junk = tier2.rip(5)

tier3, board = board.crosscut(2.5)
tier3, junk = tier3.rip(2.5)

print("now glue", base, tier2, tier3)


"""
Top Square: 2.5x2.5”
Middle Square: 5x5”
Bottom Square: 7.5x7.5”

3.5” wide. Glue Up 3 side by side

- 3 7.5” slices of 2x4 → glue up → cut down from 7” to
- 2 5” slices of 2x4 → glue up → cut down from 7” to 5”
- 1 2.5” slices of 2x4
"""
