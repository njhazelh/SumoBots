from strategies import ACTIONS
from strategies import STRATEGIES
from strategies import util

class Robot:
    """
    A Robot is a single agent within the SumoBot world. It moves according
    to its Strategy, and can be pushed by other robots if they collide.
    """

    def __init__(self, x, y, id, world, color, type):
        """
        Initialize the robot state.
        :param x: The column of the robot
        :param y: The row of the robot
        :param world: The world the robot is in.
        :param color: The color of the robot
        :param type: The strategy type of the robot.
        """
        self.id = id
        self.type = type
        self.world = world
        self.x = x
        self.y = y
        self.x_intended = None
        self.y_intended = None
        self.color = color
        self.fail_prob = 0.2
        self.last_action = None

    def reset(self, x, y):
        self.x_intended = None
        self.y_intended = None
        self.last_action = None
        self.x = x
        self.y = y

    def set_enemy(self, enemy):
        """
        Set the robot this robot is trying to push out of the ring.
        :param enemy: The enemy robot.
        """
        self.enemy = enemy

    def get_type_name(self):
        botTypeName = "UNKNOWN"

        if self.type == STRATEGIES.HUMAN:
            botTypeName = "Human"
        elif self.type == STRATEGIES.Q_LEARNING:
            botTypeName = "Q-Learning"
        elif self.type == STRATEGIES.VALUE_ITERATION:
            botTypeName = "Value Iteration"
        elif self.type == STRATEGIES.RANDOM:
            botTypeName = "Random"

        return botTypeName

    def load_strategy(self, from_store):
        """
        Load the strategy that this robot is configured to use.
        """
        self.strategy = STRATEGIES.enum_to_strategy(self, self.enemy, self.world, self.type, from_store)

    def act(self):
        """
        Act according the robot's strategy.
        :return: True if the update was completed, else False.
        """
        action = self.strategy.choose_action()
        self.update_intended_state(action)
        if action is None or action not in self.get_legal_actions():
            return False
        else:
            action = self.add_action_noise(action)
            self.apply_action(action)
            self.last_action = action
            return True

    def update_strategy(self):
        """
        Update the strategy after a move completed.
        """
        self.strategy.update()

    def get_legal_actions(self, state=None, world=None):
        """
        :return: The actions that will not end the game for this robot.
        """

        if state is None: state = self.state
        if world is None: world = self.world

        actions = []
        x, y = state
        grid = world.sumo_grid

        # Return actions for each direction that are in the arena, or are
        # terminal states
        if grid[x + 1][y] != -9 or world.is_boundary_cell(x+1,y):
            actions.append(ACTIONS.MOVE_EAST)

        if grid[x - 1][y] != -9 or world.is_boundary_cell(x-1,y):
            actions.append(ACTIONS.MOVE_WEST)

        if grid[x][y - 1] != -9 or world.is_boundary_cell(x,y-1):
            actions.append(ACTIONS.MOVE_NORTH)

        if grid[x][y + 1] != -9 or world.is_boundary_cell(x,y+1):
            actions.append(ACTIONS.MOVE_SOUTH)

        return actions

    def get_transition_model(self, world=None):
        """
        Get the transition model for this robot.
        :param world: The world to use to find this transition model. It defaults
            to self.world, but you can also pass in a world (as is done in
            qLearning).
        :return: The transition model of the robot consisting of a dictionary of
            actions.  The value of each action is another dictionary containing the actions
            that may result of trying to perform that action and their probabilities.
        """
        trans_model = {}
        if world is None:
            world = self.world
        for state in world.states:
            legal_actions = self.get_legal_actions(state, world)
            num_actions = len(legal_actions)
            # divide the prob of failure equally among the wrong actions
            p_wrong_action = self.fail_prob / (num_actions - 1)
            for action_attempt in legal_actions:
                trans_model[state, action_attempt] = {}
                for action_occur in legal_actions:
                    next_state = self.next_state(action_occur, state)
                    if action_attempt == action_occur:
                        # prob of performing the correct action
                        trans_model[(state, action_attempt)][next_state] = 1 - self.fail_prob
                    else:
                        trans_model[(state, action_attempt)][next_state] = p_wrong_action
        return trans_model

    def get_all_actions(self, world=None):
        """
        Get all the possible legal actions for every state in the world.
        :param world: The world to search in. Defaults to self.world.
        :return: A dictionary where the keys are states in world, and
            the values are lists of the legal actions at those states.
        """
        if world is None: world = self.world

        allActions = {}
        for state in world.states:
            allActions[state] = self.get_legal_actions(state, world)
        return allActions

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
        new_action = util.chooseFromDistribution(weighted_actions)
        return new_action

    def next_state(self, action, state=None):
        """
        Get the state that an action would put the robot in without mutating the
        actual robot state
        :param action: The action the robot would perform
        :return: The state the action would put the robot in.
        """
        if state is None:
            state = self.state

        x, y = state

        if action == ACTIONS.MOVE_NORTH:
            y -= 1
        elif action == ACTIONS.MOVE_SOUTH:
            y += 1
        elif action == ACTIONS.MOVE_WEST:
            x -= 1
        elif action == ACTIONS.MOVE_EAST:
            x += 1

        return x, y

    def update_intended_state(self, action):

        if action == ACTIONS.MOVE_NORTH:
            self.y_intended = self.y - 1
            self.x_intended = self.x
        elif action == ACTIONS.MOVE_SOUTH:
            self.y_intended = self.y + 1
            self.x_intended = self.x
        elif action == ACTIONS.MOVE_WEST:
            self.y_intended = self.y
            self.x_intended = self.x - 1
        elif action == ACTIONS.MOVE_EAST:
            self.y_intended = self.y
            self.x_intended = self.x + 1

    @property
    def state(self):
        """
        :return: The current state of the robot.
        """
        return self.x, self.y

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

    def intended_at(self, x, y):
        """
        What the robot attempting to go to cell (x,y)?
        """
        return x == self.x_intended and y == self.y_intended
