import pyglet
from .biome import FieldBiome
from .tilerenderer import Renderer
from .world import World, P

def test_renderer():
    window = pyglet.window.Window()
    renderer = Renderer(window)
    world = World()

    b = FieldBiome()
    b.generate()
    world.adopt_biome(b)

    @window.event
    def on_draw():
        window.clear()
        renderer.draw(world.get_tiles(P(0,0), 20, 20))

    pyglet.app.run()


if __name__ == '__main__':
    test_renderer()
