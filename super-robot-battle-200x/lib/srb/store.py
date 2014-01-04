

class Weapon(object):

    def __init__(self, power, range, speed, delay, ammo):
        self.POWER = power
        self.RANGE = range
        self.SPEED = speed
        self.DELAY = delay
        self.ammo = ammo
        self.last_fire = -delay  # can always fire at t=0

    def try_fire(self, now):
        ''' fire if it is possible '''
        if now - self.last_fire >= self.DELAY and self.ammo > 0:
            self.last_fire = now
            self.ammo -= 1
            print 'fire @ ', now
            return True
        else:
            return False

gun = Weapon(1, 400, 10, 5, 25)
cannon = Weapon(5, 50, 3, 20, 5)

class Body(object):

    def __init__(self, max_health, min_speed, max_speed):
        self.max_health = max_health
        self.min_speed = min_speed
        self.max_speed = max_speed


default_body = Body(100, -3, 5)
