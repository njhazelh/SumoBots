from strategies.Strategy import Strategy
from qLearning import QLearning

__author__ = 'Nick'


class QLearnStrategy(Strategy):
    def __init__(self, robot, otherbot, world):
        self.robot = robot
        self.otherbot = otherbot
        self.world = world
        self.Q = QLearning(world, robot, otherbot)

    def choose_action(self):
        return self.Q.getAction(self.world, self.robot)

    def update(self):
        self.Q.update(self.world, self.robot)
