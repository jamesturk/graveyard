import numpy as np
import math


class HexGrid:
    def __init__(self, w, h):
        self.grid = np.zeros((w, h))
        self.side_length = 3
        self.vskip = self.side_length * math.sin(math.radians(60))
        self.hskip = self.side_length * math.cos(math.radians(60))

    def point(self, y, x, n):
        """
                1   2
            3     0     4
                5   6
        """
        # in an even row, move over a full hex
        if y % 2:
            x = (x * (2 * self.hskip + self.side_length)) + (self.hskip + self.side_length) + (self.side_length * x)
        else:
            x = (x * (2 * self.hskip + self.side_length)) + (self.side_length) * x
        # in an odd row move over a little more

        y = y * self.vskip
        if n == 1 or n == 5:
            x += self.hskip
        elif n == 2 or n == 6:
            x += self.hskip + self.side_length
        elif n == 4:
            x += 2 * self.hskip + self.side_length
        if n == 3 or n == 4:
            y += self.vskip
        elif n == 5 or n == 6:
            y += 2 * self.vskip
        return x, y

    def points(self, x, y):
        for n in (1,2,4,6,5,3):
            yield self.point(x, y, n)

    def draw_hex(self, x, y):
        # b&w
        color = (self.grid[x][y], self.grid[x][y], self.grid[x][y])
        # color
        #color = colors[int(self.grid[x][y] * (len(colors)))]
        gl.glBegin(gl.GL_POLYGON)
        gl.glColor3f(*color)
        for p in grid.points(x, y):
            gl.glVertex2f(*p)
        gl.glEnd()

    def draw(self):
        w, h = self.grid.shape
        for x in range(w):
            for y in range(h):
                self.draw_hex(x, y)

    def neighbor(self, y, x, direction):
        if direction == 'N':
            dx, dy = 0, -2
        elif direction == 'S':
            dx, dy = 0, 2
        elif direction == 'NE':
            dx = y % 2 - 1
            dy = -1
        elif direction == 'NW':
            dx = y % 2
            dy = -1
        elif direction == 'SE':
            dx = y % 2 - 1
            dy = 1
        elif direction == 'SW':
            dx = y % 2
            dy = 1
        return (y + dy, x + dx)

import pyglet
from pyglet import gl
from pyglet.window import key
colors = [
    (1, 0, 0),
    (1, 0.7, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0.7, 1),
]

window = pyglet.window.Window(600, 600)
grid = HexGrid(20, 20)

NEIGHBORS = (
    'N', 'S',
    'SE', 'SW',
    'NE', 'NW'
)

cx, cy = 7, 9

def update_grid():
    grid.grid[...] = 0
    grid.grid[cx, cy] = 1
    for d in NEIGHBORS:
        x, y = grid.neighbor(cx, cy, d)
        grid.grid[x, y] = 0.8
        x, y = grid.neighbor(x, y, d)
        grid.grid[x, y] = 0.6
        x, y = grid.neighbor(x, y, d)
        grid.grid[x, y] = 0.4

@window.event
def on_key_press(symbol, modifiers):
    print('key press', symbol)
    if symbol == key.NUM_8:
        dir = 'N'
    elif symbol == key.NUM_2:
        dir = 'S'

    cx, cy = grid.neighbor(cx, cy, dir)

@window.event
def on_key_press(symbol, modifiers):
    print('release')

@window.event
def on_mouse_press(x, y, button, modifiers):
    print('The mouse button was pressed.')

@window.event
def on_draw():
    update_grid()
    window.clear()
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, 200, 200, 0, 0, 1)
    grid.draw()

pyglet.app.run()
