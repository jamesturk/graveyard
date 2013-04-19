import re
# input
# T - number of test cases
# N - number of buttons to be pressed
#   O|B n  - Orange or Blue and button to be pressed


example = """3
4 O 2 B 1 B 2 O 4
3 O 5 O 8 B 100
2 B 2 B 1"""


def process_input(input):
    for i, line in enumerate(input.splitlines()[1:]):
        print "Case #%d: %d" % (i+1, robot_course(line))

def get_next_pos(course, cdone, robot):
    for r, n in course[cdone:]:
        if r == robot:
            return n

def robot_course(input):
    course = []
    # don't need the first part
    input = input[2:]
    for r,n in re.findall('([BO]) (\d+)', input):
        course.append((r, int(n)))

    t = 0
    cdone = 0
    pos = {'O': 1, 'B': 1}
    dest = {'O': get_next_pos(course, cdone, 'O'),
            'B': get_next_pos(course, cdone, 'B')}

    while cdone < len(course):
        t += 1
        push = False

        for r in 'OB':
            if dest[r]:
                if dest[r] == pos[r]:
                    if course[cdone][0] == r:
                        # push this button!
                        push = r
                    else:
                        pass # wait
                elif pos[r] < dest[r]:
                    pos[r] += 1
                elif pos[r] > dest[r]:
                    pos[r] -= 1

        if push:
            cdone += 1
            dest['O'] = get_next_pos(course, cdone, 'O')
            dest['B'] = get_next_pos(course, cdone, 'B')

    return t

if __name__ == '__main__':
    process_input(open('A-large.in').read())
