import time
from strategies import STRATEGIES

__author__ = 'Nick'

class Robot:
    def __init__(self, x, y, world, color, type):
        self.strategy = STRATEGIES.enum_to_strategy(world, type)
        self.type = type
        self.world = world
        self.x = x
        self.y = y
        self.color = color

    def update(self):
        time.sleep(.5)

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def is_human(self):
        return self.type == STRATEGIES.HUMAN
