import sys
import os

from cocos.director import *
from cocos.menu import *
from cocos.scene import *

from srb.util import Point
from srb.arena import Robot, Arena
from srb.editor import Editor

class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__("Main Menu")

        self.menu_valign = CENTER
        self.menu_halign = LEFT

        self.font_title = "Impact"
        self.font_items = "ProggySquareTT"
        self.font_items_selected = "ProggySquareTT"
        
        # font sizes
        self.font_title_size = 32
        self.font_items_size = 18
        self.font_items_selected_size = 24

        self.font_items_selected_color = (128, 255, 128, 255)

        self.add_item(MenuItem('New Game', self.on_new_game))
        self.add_item(MenuItem('Continue', self.on_continue))
        self.add_item(MenuItem('Exit', self.on_quit))

        self.build_items()

    def on_new_game(self):
        # TODO: for now this will point directly to lab
        self.switch_to(3)

    def on_continue(self):
        self.switch_to(2)

    def on_quit(self):
        sys.exit()

class ContinueMenu(Menu):
    def __init__(self):
        super(ContinueMenu, self).__init__("Load Game")

        self.menu_valign = CENTER
        self.menu_halign = LEFT

        self.font_title = "Impact"
        self.font_items = "ProggySquareTT"
        self.font_items_selected = "ProggySquareTT"

        # font sizes
        self.font_title_size = 32
        self.font_items_size = 18
        self.font_items_selected_size = 24

        self.font_items_selected_color = (128, 255, 128, 255)

        #
        # TODO: get a list of savegames here & add them
        #

        self.add_item(MenuItem('Back', self.on_quit))

        self.build_items()

    def on_quit(self):
        self.switch_to(1)

class LabMenu(Menu):
    def __init__(self):
        super(LabMenu, self).__init__("Laboratory")

        self.menu_valign = CENTER
        self.menu_halign = LEFT

        self.font_title = "Impact"
        self.font_items = "ProggySquareTT"
        self.font_items_selected = "ProggySquareTT"

        # font sizes
        self.font_title_size = 32
        self.font_items_size = 18
        self.font_items_selected_size = 24

        self.font_items_selected_color = (128, 255, 128, 255)

        self.add_item(MenuItem('Fight', self.on_fight))
        self.add_item(MenuItem('Reprogram', self.on_reprogram))
        self.add_item(MenuItem('Store', self.on_store))
        self.add_item(MenuItem('Save', self.on_save))
        self.add_item(MenuItem('Back', self.on_quit))

        self.build_items()

    def on_fight(self):
        self.switch_to(4)

    def on_reprogram(self):
        director.run(Scene(Editor()))

    def on_store(self):
        print "on_store"

    def on_save(self):
        print "on_save"

    def on_quit(self):
        self.switch_to(1)

class FightMenu(Menu):
    def __init__(self):
        super(FightMenu, self).__init__("Fight")

        self.menu_valign = CENTER
        self.menu_halign = LEFT

        self.font_title = "Impact"
        self.font_items = "ProggySquareTT"
        self.font_items_selected = "ProggySquareTT"

        # font sizes
        self.font_title_size = 32
        self.font_items_size = 18
        self.font_items_selected_size = 24

        self.font_items_selected_color = (128, 255, 128, 255)

        #
        # TODO: get a list of bots to fight & add them
        #

        self.add_item(MenuItem('Go!', self.on_fight))
        self.add_item(MenuItem('Back', self.on_quit))

        self.build_items()

    def on_fight(self):
        player = Robot(Point(300,100), 135, 1)
        player._script = """
robot.heading += 1
if robot.heading % 15 == 0:
    robot.fire_left_weapon()
"""
        cpu = Robot(Point(0,0), 0, 2)
        cpu._script = """
if robot.pos.x == 0:
    robot.heading = 0
    robot.fire_left_weapon()
elif robot.pos.x == ARENA_WIDTH:
    robot.heading = 180
    robot.fire_left_weapon()
"""
        director.run(Scene(Arena(player, cpu)))

    def on_quit(self):
        self.switch_to(3)
