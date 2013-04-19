from collections import defaultdict

example = """5
0 0 2 EA
1 QRI 0 4 RRQR
1 QFT 1 QF 7 FAQFDFQ
1 EEZ 1 QE 7 QEEEERA
0 1 QW 2 QW"""

def process_input(input):
    for i, line in enumerate(input.splitlines()[1:]):
        print "Case #%d: [%s]" % (i+1, magicka(line))

def magicka(line):
    pieces = line.split()
    combinations = {}
    oppositions = defaultdict(list)

    # process all combinations
    c = int(pieces.pop(0))
    while c:
        c -= 1
        combo = pieces.pop(0)
        combinations[frozenset(combo[:2])] = combo[2]

    # process all oppositions
    d = int(pieces.pop(0))
    while d:
        d -= 1
        opp = pieces.pop(0)
        oppositions[opp[0]].append(opp[1])
        oppositions[opp[1]].append(opp[0])

    # shed number of letters in input
    pieces.pop(0)
    elements = pieces.pop(0)

    # process inputs
    result = []
    for e in elements:
        if result:
            # do a combination
            combo = combinations.get(frozenset((e, result[-1])))
            if combo:
                result[-1] = combo
                continue

            has_opp = False
            for opposed in oppositions[e]:
                if opposed in result:
                    has_opp = True
                    break
            if has_opp:
                result = []
                continue

        result.append(e)

    return ', '.join(result)


process_input(open('B-large.in').read())
