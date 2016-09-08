import colorsys
import random
from numpy import array
from pyglet.gl import *
import pyglet
from mingus.containers import Note, NoteContainer, Bar
from mingus.midi import MidiFileOut, fluidsynth
from mingus.extra import LilyPond

class Grid(object):

    pad_size = 2
    active_col = 0

    def __init__(self, size, physical_size):
        self.size = size
        self.clear()
        self.square_size = physical_size / self.size
        self.y_offset = self.x_offset = self.square_size

    def clear(self):
        self._grid = array([[0.0]*self.size]*self.size)

    def randomize(self, n=50):
        for x in xrange(50):
            self._grid[random.randint(0,self.size-1), random.randint(0,self.size-1)] = 1

    def get_neighbors(self, x, y):
        offsets = [(-1,-1), (-1, 0), (-1, 1),
                   (0,-1), (0,1),
                   (1,-1), (1, 0), (1, 1)]
        coords = [((x+dx)%self.size, (y+dy)%self.size) for dx,dy in offsets]
        return sum([self._grid[x,y] > 0.5 for (x,y) in coords])


    def update_grid(self):
        new_grid = array(self._grid)

        for x in range(self.size):
            for y in range(self.size):
                neighbors = self.get_neighbors(x,y)
                alive = self._grid[x,y] > 0.5
                if not alive:
                    new_grid[x,y] = 0
                if alive and (neighbors < 2 or neighbors > 3):
                    new_grid[x,y] = 0.2
                elif not alive and neighbors == 3:
                    new_grid[x,y] = 1
                if alive and new_grid[x,y] > 0.5:
                    new_grid[x,y] = min(self._grid[x,y]+0.1, 2.0)

        self._grid = new_grid

    ## musical ##

    def row_to_note_simple(self, row):
        base_note = 48
        note = Note()
        note.from_int(row+base_note)
        return note

    def row_to_note_pentatonic(self, row):
        scale = 'CDEGA'
        initial = 4
        return Note('%s-%s' % (scale[row%5], row/5+initial))

    row_to_note = row_to_note_pentatonic

    def column_to_notes(self, col):
        notes = []
        base_note = 48
        indices = filter(lambda x:x[1], enumerate(self._grid[:,col]))
        notes = [self.row_to_note(n[0]) for n in indices]
        return notes

    def play_column(self):
        notes = self.column_to_notes(self.active_col)
        fluidsynth.play_NoteContainer(notes)

    def grid_to_bar(self):
        bar = Bar()
        bar.length = self.size
        for col in xrange(self.size):
            notes = self.column_to_notes(col)
            bar.place_notes(notes, 4)
        return bar

    ## graphical ##

    def rc_to_xy(self, r, c):
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            pass
        return (self.x_offset + c*(self.square_size+self.pad_size),
                self.y_offset + r*(self.square_size+self.pad_size))

    def xy_to_rc(self, x, y):
        r = (y - self.y_offset) / (self.square_size+self.pad_size)
        c = (x - self.x_offset) / (self.square_size+self.pad_size)
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            raise ValueError('mouse pointer outside of grid boundaries')
        return r,c

    def draw_grid(self):
        for r, row in enumerate(self._grid):
            hue = float(r)/self.size
            for c, cell in enumerate(row):
                sat = 0.5 * cell
                val = 0.5
                if c == self.active_col:
                    val = 0.9
                elif c == self.active_col - 1:
                    val = 0.75
                elif c == self.active_col - 2:
                    val = 0.6
                color = colorsys.hsv_to_rgb(hue, sat, val)
                x,y = self.rc_to_xy(r, c)
                glPushMatrix()
                glColor3f(*color)
                glTranslatef(x, y, 0)
                glBegin(GL_QUADS)
                glVertex2f(0, 0)
                glVertex2f(0, self.square_size)
                glVertex2f(self.square_size, self.square_size)
                glVertex2f(self.square_size, 0)
                glEnd()
                glPopMatrix()

EV_OFF, EV_GRID, EV_COLUMN = range(3)

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.grid = Grid(16, 320)
        self.paused = True
        self.evolution_style = EV_OFF
        pyglet.clock.schedule_interval(self.update, 0.25)

        x = self.width - 10
        self.r_label = pyglet.text.Label('R - randomize', font_size=16,
                                         x=x, y=160, anchor_x='right')
        self.c_label = pyglet.text.Label('C - clear', font_size=16,
                                         x=x, y=190, anchor_x='right')
        self.p_label = pyglet.text.Label('P - play', font_size=16,
                                         x=x, y=220, anchor_x='right')
        self.e_label = pyglet.text.Label('E - evolution | off', font_size=16,
                                         x=x, y=250, anchor_x='right')

    def on_draw(self):
        self.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        self.grid.draw_grid()
        self.r_label.draw()
        self.c_label.draw()
        self.p_label.draw()
        self.e_label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.M:
            bar = self.grid.grid_to_bar()
            MidiFileOut.write_Bar('life.mid', bar)
            lps = LilyPond.from_Bar(bar)
            print lps
        elif symbol == pyglet.window.key.R:
            self.grid.randomize()
        elif symbol == pyglet.window.key.P:
            self.paused = not self.paused
            self.p_label.text = 'P - play' if self.paused else 'P - pause'
        elif symbol == pyglet.window.key.C:
            self.grid.clear()
        elif symbol == pyglet.window.key.E:
            self.evolution_style += 1
            if self.evolution_style >= 3:
                self.evolution_style = 0
            self.e_label.text = 'E - evolution | ' + ['off', 'on', 'fast'][self.evolution_style]

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            try:
                r, c = self.grid.xy_to_rc(x, y)
                self.grid._grid[r,c] = 0 if self.grid._grid[r,c] else 1
            except ValueError:
                pass

    def update(self, dt):
        if not self.paused:

            if self.evolution_style == EV_COLUMN:
                self.grid.update_grid()
            self.grid.active_col += 1


            if self.grid.active_col >= self.grid.size:
                self.grid.active_col = 0
                if self.evolution_style == EV_GRID:
                    self.grid.update_grid()
            self.grid.play_column()

def main():
    fluidsynth.init('Rhodes_73.SF2', 'pulseaudio')
    window = MainWindow()
    pyglet.app.run()

if __name__ == '__main__':
    main()
