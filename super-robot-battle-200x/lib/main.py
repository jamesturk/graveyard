'''Game main module.

Contains the entry point used by the run_game.py script.
'''

import cocos
from cocos.director import director
from cocos.layer import *

from pyglet import gl
from pyglet import media
import pyglet
pyglet.resource.path.append('data')
pyglet.resource.reindex()

from srb.menus import *
from srb.title import *

def main():
    director.init(width=1024, height=768, caption='Super Robot Battle 200X')
#    theme = media.load('data/song1.mp3', streaming=True)
#    theme.play()
    # 0 - title
    # 1 - main
    # 2 - continue
    # 3 - lab
    # 4 - fight
    director.run(Scene(ColorLayer(0.00,0.0,0.0,1.0), MultiplexLayer(Title(), MainMenu(), ContinueMenu(), LabMenu(), FightMenu())))
