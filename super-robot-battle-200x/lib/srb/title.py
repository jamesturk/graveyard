from cocos.layer import *
from cocos.actions import *

from pyglet import font, image, sprite, clock
import pyglet

class Title(Layer):
    def __init__(self):
        super(Title, self).__init__()

        image = pyglet.resource.image('title.png')
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2

        self.logo = sprite.Sprite(image, x=512, y=384)

        # the blinking text "press any key to continue"
        img2 = pyglet.resource.image('blinking_text.png')
        
        img2.anchor_x = img2.width / 2
        img2.anchor_y = img2.height / 2

        self.blinking_text = sprite.Sprite(img2, x=523, y=150)

        # blink our text every .5 seconds
        self.render_blink = True
        clock.schedule_interval(self.blink, 0.5)

    def blink(self, dt):
        self.render_blink = not self.render_blink

    def on_key_press(self, symbol, modifiers):
        self.switch_to(1)
        
    def draw(self):
        self.logo.draw()
        
        if self.render_blink:
            self.blinking_text.draw()
