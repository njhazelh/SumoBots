import random
import ACTIONS
from Strategy import Strategy

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
        if grid[x - 1][y] != -9:
            actions.append(ACTIONS.MOVE_WEST)
        if grid[x][y - 1] != -9:
            actions.append(ACTIONS.MOVE_NORTH)
        if grid[x][y + 1] != -9:
            actions.append(ACTIONS.MOVE_SOUTH)

        choice = random.choice(actions)
        return choice

    def __str__(self):
        return "Random"

