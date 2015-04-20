import ACTIONS
from strategies import STRATEGIES
import util

__author__ = 'Nick'

NORTH = 0
SOUTH = 1
WEST = 2
EAST = 3


class Robot:
    """
    A Robot is a single agent within the SumoBot world. It moves according
    to its Strategy, and can be pushed by other robots if they collide.
    """

    def __init__(self, x, y, world, color, type):
        """
        Initialize the robot state.
        :param x: The column of the robot
        :param y: The row of the robot
        :param world: The world the robot is in.
        :param color: The color of the robot
        :param type: The strategy type of the robot.
        """
        self.strategy = STRATEGIES.enum_to_strategy(self, world, type)
        self.type = type
        self.world = world
        self.x = x
        self.y = y
        self.color = color
        self.fail_prob = 0.2
        self.last_action = None

    def update(self):
        """
        Act according the robot's strategy.
        :return: True if the update was completed, else False.
        """
        action = self.strategy.choose_action()
        if action is None:
            return False
        else:
            action = self.add_action_noise(action)
            self.apply_action(action)
            self.last_action = action
            return True

    def get_legal_actions(self):
        """
        :return: The actions that will not end the game for this robot.
        """
        actions = []
        x = self.x
        y = self.y
        grid = self.world.sumo_grid

        # For now just return 1 space to the 'West', 'East', 'North', 'South'
        if grid[x + 1][y] != -9:
            actions.append(ACTIONS.MOVE_EAST)

        if grid[x - 1][y] != -9:
            actions.append(ACTIONS.MOVE_WEST)

        if grid[x][y - 1] != -9:
            actions.append(ACTIONS.MOVE_NORTH)

        if grid[x][y + 1] != -9:
            actions.append(ACTIONS.MOVE_SOUTH)

        return actions

    def add_action_noise(self, action):
        """
        Add a little randomness to action performance in accordance to fail_prob
        :param action: The action to randomize.
        :return: The randomized action.
        """
        legal_actions = self.get_legal_actions()
        weighted_actions = []
        distribution_spread = self.fail_prob / (len(legal_actions) - 1)

        for legal_action in legal_actions:
            if legal_action == action:
                weighted_actions.append(((1 - self.fail_prob), legal_action))
            else:
                weighted_actions.append((distribution_spread, legal_action))

        return util.chooseFromDistribution(weighted_actions)

    def apply_action(self, action):
        """
        Apply an action to the robot.
        :param action: The action to apply
        """
        if action == ACTIONS.MOVE_NORTH:
            self.y -= 1
        elif action == ACTIONS.MOVE_SOUTH:
            self.y += 1
        elif action == ACTIONS.MOVE_WEST:
            self.x -= 1
        elif action == ACTIONS.MOVE_EAST:
            self.x += 1
        else:
            raise Exception("%s is not a action" % (action))

    def collides_with(self, other):
        """
        Is this robot at the same location as other?
        :param other: The other robot to check
        :return: True if they're at the same location, else False.
        """
        return self.is_at(other.x, other.y)

    def is_at(self, x, y):
        """
        Is this robot at the col, row coordinates of x, y?
        :param x: The column the robot is in.
        :param y: The row the robot is in.
        :return: True if the robot's row and column are x and y respectively.
        """
        return self.x == x and self.y == y
