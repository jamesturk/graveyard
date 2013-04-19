import sys
import operator

example = """3
2
2 1
3
1 3 2
4
2 1 4 3"""

def process_input(input):
    # only need every other line, skipping first line
    for i, line in enumerate(input.splitlines()[::2][1:]):
        print "Case #%d: %.6d" % (i+1, goro(line))

def goro(line):
    array = line.split()
    
