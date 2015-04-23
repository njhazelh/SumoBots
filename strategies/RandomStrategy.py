import random
import ACTIONS
from Strategy import Strategy

__author__ = 'Nick'

class RandomStrategy(Strategy):
    def __init__(self, robot, world):
        self.robot = robot
        self.world = world

    def choose_action(self):
        actions = []

        x, y = self.robot.state
        grid = self.world.sumo_grid

        if grid[x + 1][y] != -9:
            actions.append(ACTIONS.MOVE_EAST)
        elif grid[x - 1][y] != -9:
            actions.append(ACTIONS.MOVE_WEST)
        elif grid[x][y - 1] != -9:
            actions.append(ACTIONS.MOVE_NORTH)
        elif grid[x][y + 1] != -9:
            actions.append(ACTIONS.MOVE_SOUTH)

        return random.choice(actions)

    def __str__(self):
        return "Random"

