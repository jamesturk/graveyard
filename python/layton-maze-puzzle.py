"""
written for Erin, July 2010

find path through maze touching the most stops

for a professor layton puzzle
"""

import copy

class Grid(object):

    def __init__(self, walls):
        self.visited = [[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]]
        self.walls = walls
        self.moves = []
        self.x = 0
        self.y = 0

    def valid_move(self, direction):
        # if walls aren't blocking the move
        if direction not in self.walls[self.y][self.x]:
            nx, ny = self.get_new_pos(direction)
            return not self.visited[ny][nx]
        return False

    def get_new_pos(self, direction):
        nx = self.x
        ny = self.y
        if direction == 'l':
            nx -= 1
        elif direction == 'r':
            nx += 1
        elif direction == 'u':
            ny -= 1
        elif direction == 'd':
            ny += 1
        else:
            raise ValueError('invalid direction')
        return nx, ny

    def move(self, direction):
        if self.valid_move(direction):
            self.x, self.y = self.get_new_pos(direction)
            self.visited[self.y][self.x] = True
            self.moves.append(direction)
        else:
            raise ValueError('invalid move')

    def valid_moves(self):
        return [d for d in 'udlr' if self.valid_move(d)]

    def solved(self):
        return self.x == 0 and self.y == 4

    def children(self):
        for move in self.valid_moves():
            newcopy = copy.deepcopy(self)
            newcopy.move(move)
            yield newcopy

g = Grid(
    [ ['ul', 'ud', 'u', 'ud', 'ur'],
    ['l', 'u', 'd', 'u', 'r'],
    ['lr', 'l', 'ud', 'r', 'lr'],
    ['l', 'd', 'u', 'd', 'r'],
    ['ld', 'ud', 'd', 'ud', 'rd']]
)
g.x = 4
g.visited[0][4] = True

def solver(initial):
    state_queue = [initial]

    while state_queue:
        cur = state_queue.pop(0)
        if cur.solved():
            print len(cur.moves), ''.join(cur.moves)
        else:
            for child in cur.children():
                state_queue.append(child)

