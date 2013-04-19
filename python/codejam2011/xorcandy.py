import sys
import operator

sys.setrecursionlimit(100000)

example = """2
5
1 2 3 4 5
3
3 5 6"""

def process_input(input):
    # only need every other line, skipping first line
    for i, line in enumerate(input.splitlines()[::2][1:]):
        print "Case #%d: %s" % (i+1, steal_candy(line))

def patrick_val(candy):
    return reduce(operator.xor, candy)

def all_piles(pile):
    if len(pile) == 1:
        yield pile
    else:
        for i, item in enumerate(pile):
            for subpile in all_piles(pile[i+1:]):
                yield [item] + subpile
            yield [item]

def other_pile(mainpile, subpile):
    retpile = list(mainpile)
    for c in subpile:
        retpile.remove(c)
    return retpile

def steal_candy(candy):
    candy = [int(c) for c in candy.split()]

    equilibrium = []

    for sean_pile in all_piles(candy):
        patrick_pile = other_pile(candy, sean_pile)
        if patrick_pile:
            #print patrick_pile, patrick_val(patrick_pile), sean_pile, patrick_val(sean_pile)
            if patrick_val(sean_pile) == patrick_val(patrick_pile):
                equilibrium.append(sum(sean_pile))

    if equilibrium:
        return max(equilibrium)
    else:
        return "NO"

process_input(open('C-large.in').read())
