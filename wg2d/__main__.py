import pyglet
from .tilerenderer import Renderer

def test_renderer():
    window = pyglet.window.Window()
    renderer = Renderer(window)

    tiles = [[1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
             [1,1,1,1,1,1,1,1],
            ]

    @window.event
    def on_draw():
        window.clear()
        renderer.draw(tiles)

    pyglet.app.run()


if __name__ == '__main__':
    test_renderer()
