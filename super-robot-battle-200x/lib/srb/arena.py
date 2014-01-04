'''
    arena.py - Objects used within the arena portion of the game.
'''

from math import sin, cos, tan, atan2, degrees, radians, sqrt
from random import randint
from copy import copy

import cocos
from cocos.director import director
import pyglet
from pyglet.gl import *

from util import *
import store
from safe_exec import safe_exec

class ArenaObject(object):

    HALF_WIDTH = 1
    HALF_HEIGHT = 1
    RADIUS = 2

    def __init__(self, position, heading, speed):
        self.position = position
        self.heading = heading
        self.speed = speed

    def get_center(self):
        return Point(self.position.x + self.HALF_WIDTH,
                     self.position.y + self.HALF_HEIGHT)
    center = property(get_center)

    def move(self, dt):
        self.position.x += self.speed * cos(radians(self.heading))
        self.position.y += self.speed * sin(radians(self.heading))

    def unmove(self, dt):
        self.position.x -= self.speed * cos(radians(self.heading))
        self.position.y -= self.speed * sin(radians(self.heading))

    def collides_with(self, obj):
        collision = distance(self.center, obj.center) < (self.RADIUS+obj.RADIUS)
        return collision


class Projectile(ArenaObject):
    '''
        Projectile in motion in the arena
    '''

    HALF_WIDTH=1
    HALF_HEIGHT=1
    RADIUS=1

    def __init__(self, from_robot, weapon):
        super(Projectile, self).__init__(copy(from_robot.position),
                                         from_robot.heading, weapon.SPEED)
        self.from_robot = from_robot
        self._from_loc = copy(from_robot.position)
        self.power = weapon.POWER
        self._range = weapon.RANGE

        self.image = pyglet.resource.image('shot.png')
        self.image.anchor_x = self.HALF_WIDTH
        self.image.anchor_y = self.HALF_HEIGHT
        self.sprite = pyglet.sprite.Sprite(self.image)

    def in_range(self):
        return distance(self.position, self._from_loc) < self._range

    def draw(self):
        glPushMatrix()
        self.sprite.set_position(self.position.x, self.position.y)
        self.sprite.rotation = 90-self.heading
        self.sprite.draw()
        glPopMatrix()

class RobotController(object):

    def __init__(self, robot):
        self.__robot = robot

    ## read only attributes ##

    MIN_SPEED = property(lambda self: self.__robot.body.min_speed)
    MAX_SPEED = property(lambda self: self.__robot.body.max_speed)
    pos = property(lambda self: self.__robot.position)
    health = property(lambda self: self.__robot.health)

    ## read only enemy attributes ##

    enemy_spotted = property(lambda self: self.__robot.enemy_spotted)
    latest_enemy_pos = property(lambda self: self.__robot.enemy_position)
    latest_enemy_heading = property(lambda self: self.__robot.enemy_heading)

    ## read-write attributes ##

    def set_speed(self, speed):
        ''' set speed within bounds of MIN_SPEED and MAX_SPEED '''
        self.__robot._speed = constrain(speed, self.body.min_speed,
                                               self.body.max_speed)

    speed = property(lambda self: self.__robot._speed, set_speed)

    def set_heading(self, heading):
        ''' set speed within bounds of 0 and 360 '''
        self.__robot.heading = heading % 360

    heading = property(lambda self: self.__robot.heading, set_heading)

    def goto(self, point):
        ''' a helper to adjust heading to point at x,y '''
        self.__heading = degrees(atan2(point.y-self.position.y,
                                       point.x-self.position.x))

    ## weaponry ##

    def fire_left_weapon(self):
        self.__robot.fire_left_weapon()

    def fire_right_weapon(self):
        self.__robot.fire_left_weapon()

class Robot(ArenaObject):

    HALF_WIDTH=24
    HALF_HEIGHT=26
    RADIUS=36

    def __init__(self, position, heading, speed):
        super(Robot, self).__init__(position, heading, speed)

        self.body = store.default_body
        self.left_arm = store.gun
        self.right_arm = store.cannon

        self.health = self.body.max_health

        self.last_shot = None

        self.enemy_spotted = False
        self.enemy_position = (0,0)
        self.enemy_heading = 0

        self.image = pyglet.resource.image('robot.png')
        self.image.anchor_x = self.HALF_WIDTH
        self.image.anchor_y = self.HALF_HEIGHT
        self.sprite = pyglet.sprite.Sprite(self.image)

        self._script = 'pass'

        self.controller = RobotController(self)

    def run_script(self, environment):
        safe_exec(self._script, environment)

    def decrease_health(self, amount):
        if amount > 0:
            # don't go below 0
            self.health -= min(self.health, amount)

    def alive(self, amount):
        return self.health > 0

    def fire_left_weapon(self):
        self.last_shot = self.left_arm

    def fire_right_weapon(self):
        self.last_shot = self.right_arm

    def draw(self):
        glPushMatrix()
        self.sprite.set_position(self.position.x, self.position.y)
        self.sprite.rotation = 90-self.heading
        self.sprite.draw()
        glPopMatrix()

class Arena(cocos.layer.Layer):
    '''
        Arena is where most the actual game occurs.

        Two robots enter, only one will emerge.
    '''

    def __init__(self, player1, player2):
        super(Arena, self).__init__()
        self.WIDTH = 400
        self.HEIGHT = 400
        self.TIME_LIMIT = 100
        self.time = 0
        self.robots = [player1, player2]
        self.projectiles = []

        # both players get the same env for now we're experimenting with if we
        # want tampering with the environment to be allowed or not
        self.script_env = {'ARENA_WIDTH': self.WIDTH,
                           'ARENA_HEIGHT': self.HEIGHT,
                           'rand': randint,
                           'sin': sin,
                           'cos': cos,
                           'tan': tan}

        pyglet.clock.schedule_interval(self.update, 0.01)

    def update(self, dt):

        self.time += 1

        for robot in self.robots:
            # setup environment and run script
            self.script_env['robot'] = robot.controller
            self.script_env['curtime'] = lambda: self.time
            robot.run_script(self.script_env)

            # update movement and do collision detection
            robot.move(dt)
            robot.position.x = constrain(robot.position.x, 0, self.WIDTH)
            robot.position.y = constrain(robot.position.y, 0, self.HEIGHT)
            for opponent in self.robots:
                if robot != opponent and robot.collides_with(opponent):
                    robot.unmove(dt)

            # add new shot
            if robot.last_shot and robot.last_shot.try_fire(self.time):
                self.projectiles.append(Projectile(robot, robot.last_shot))
                robot.last_shot = None

            # update projectiles
            for p in self.projectiles:
                p.move(dt)
                if p.collides_with(robot) and p.from_robot != robot:
                    robot.decrease_health(p.power)
                    self.projectiles.remove(p)

                if (p.position.x < 0 or p.position.x > self.WIDTH or
                    p.position.y < 0 or p.position.y > self.HEIGHT or
                    not p.in_range()):
                    self.projectiles.remove(p)


    def draw(self):
        glPushMatrix()
        glTranslatef(50,50,0)
        for robot in self.robots:
            robot.draw()
        for projectile in self.projectiles:
            projectile.draw()
        glPopMatrix()

if __name__ == '__main__':
    pyglet.resource.path = ['../../data']
    pyglet.resource.reindex()
    director.init()
    player = Robot(Point(300,100), 135, 1)
    player._script = """
robot.heading += 1
#if robot.heading % 15 == 0:
    #robot.fire_left_weapon()
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
    director.run(cocos.scene.Scene(Arena(player, cpu)))
