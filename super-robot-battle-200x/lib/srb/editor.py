'''
    editor.py - The robot script text editor.
'''

import pyglet
from pyglet.window import Window
from pyglet.text.layout import IncrementalTextLayout, TextLayout
from pyglet.text.caret import Caret
from pyglet.text.document import FormattedDocument
from pyglet.graphics import Batch
from cocos.layer import Layer
from cocos.director import *

class Editor(Layer):
    def __init__(self):
        super(Editor, self).__init__()
        
        self.doc = FormattedDocument('<b>testing</b> testing testing')
        self.doc.set_style(0, 1000, {'font_name': 'ProggySquareTT'})  
        
        self.itlo = IncrementalTextLayout(self.doc, 1024, 750, multiline=True, batch=self.batch)
        self.itlo.x = 0
        self.itlo.y = 750
        caret = Caret(self.itlo)
        caret.visible = True
        caret.color = (100, 255, 0)
        
        director.window.push_handlers(caret)
        
        
    
    def draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.batch.draw()