import pyglet
from .biome import FieldBiome
from .tilerenderer import Renderer

def test_renderer():
    window = pyglet.window.Window()
    renderer = Renderer(window)
    b = FieldBiome()
    b.generate()

    @window.event
    def on_draw():
        window.clear()
        renderer.draw(b.tiles)

    pyglet.app.run()


if __name__ == '__main__':
    test_renderer()
