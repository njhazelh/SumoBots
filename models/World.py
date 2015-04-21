from strategies import ACTIONS
from models.Robot import Robot
import WORLD_STATES
from strategies import STRATEGIES

__author__ = 'Nick'


class World:
    """
    World is the world in which SumoBots fight.  It is configured as a 2D grid with a
    ring inside the grid.  Robots want to say inside the ring, and push others out.
    """

    def __init__(self, config):
        """
        Init the World state
        :param config: The configuration settings of the world.
            This should follow the following format:
                {1: ROBOT1_TYPE, 2: ROBOT2_TYPE}
        """
        self.debug = False
        self.cols = 15
        self.rows = 15
        self.ring_radius = 4
        self.states = []
        self.sumo_grid = []
        self.game_over = False
        self.state = WORLD_STATES.COUNT_DOWN
        self.count = 3
        self.key_event = None
        self.gamma = 0.3
        self.delta = 0.1
        self.alpha = 0.5
        self.epsilon = 0.5

        self.init_grid()

        self.bot1 = Robot(x=self.cols / 2 - 3, y=self.rows / 2,
                          id=1, world=self, color="#a00", type=config[1])
        self.bot2 = Robot(x=self.cols / 2 + 3, y=self.rows / 2,
                          id=2, world=self, color="#0a0", type=config[2])
        self.bot1.set_enemy(self.bot2)
        self.bot2.set_enemy(self.bot1)
        self.bot1.load_strategy()
        self.bot2.load_strategy()

        if config[1] == STRATEGIES.HUMAN or config[2] != STRATEGIES.HUMAN:
            self.current_player = 1
        else:
            self.current_player = 2


    def init_grid(self):
        """
        Initialize the cell values of the sumo Grid.
        Values within bounds are 0.
        Values out of bounds are -9.
        """
        # Initialize 2D array to 0
        for row in xrange(self.rows):
            self.sumo_grid += [[0] * self.cols]

        # Find the center of the grid
        cx = (self.cols - 1) / 2.0
        cy = (self.rows - 1) / 2.0

        # Set invalid out-of-bounds areas and record in-bound states
        for row in range(self.rows):
            for col in range(self.cols):
                dCenter = ((col - cx) ** 2 + (row - cy) ** 2) ** 0.5
                if round(dCenter) > self.ring_radius:
                    self.sumo_grid[row][col] = -9
                self.states.append((row, col))

    def get_states(self):
        return self.states

    def update(self):
        """
        Update the state of the world
        :return: True if the update completed, else False.
        """
        if self.state == WORLD_STATES.COUNT_DOWN:
            # Perform Count Down.
            self.count -= 1
            if self.count == -1:
                self.state = WORLD_STATES.PLAYING
            return True
        elif self.state == WORLD_STATES.PLAYING:
            # Advance the game state
            if self.current_player == 1 and self.bot1.act():
                # It's robot 1's turn and the turn completed successfully
                self.apply_rules(self.bot1, self.bot2)
                self.bot1.update_strategy()
                self.current_player = 2
                self.key_event = None
                return True
            elif self.current_player == 2 and self.bot2.act():
                # It's robot 2's turn and the turn completed successfully
                self.apply_rules(self.bot2, self.bot1)
                self.bot2.update_strategy()
                self.current_player = 1
                self.key_event = None
                return True
            else:
                # The current robot's turn did not complete.
                return False
        elif self.state == WORLD_STATES.GAME_OVER:
            # The game is finished.
            return True
        else:
            raise Exception("World in an unknown state: %s" % (self.state))

    def apply_rules(self, moved_bot, other_bot):
        """
        Check for collisions and game over.
        :param moved_bot: The bot that just moved.
        :param other_bot: The bot that will move next.
        """
        if moved_bot.collides_with(other_bot):
            other_bot.apply_action(moved_bot.last_action)

        if self.sumo_grid[other_bot.x][other_bot.y] == -9:
            self.game_over = True
            self.state = WORLD_STATES.GAME_OVER

        if self.sumo_grid[moved_bot.x][moved_bot.y] == -9:
            self.game_over = True
            self.state = WORLD_STATES.GAME_OVER

    def on_key(self, event):
        """
        Record a key event should it be needed.
        :param event: The event that just happened
        """
        self.key_event = event

    def pushable(self, action):
        drow = 0
        dcol = 0
        if action == ACTIONS.MOVE_NORTH:
            drow = -1
        elif action == ACTIONS.MOVE_SOUTH:
            drow = 1
        elif action == ACTIONS.MOVE_EAST:
            dcol = 1
        elif action == ACTIONS.MOVE_WEST:
            dcol = -1

        if self.current_player == 1:
            pushing_bot = self.bot1
            pushed_bot = self.bot2
        else:
            pushing_bot = self.bot2
            pushed_bot = self.bot1

        nextY = pushing_bot.y + drow
        nextX = pushing_bot.x + dcol
        return pushed_bot.is_at(nextX, nextY)

    def can_push_toward_edge(self, action):
        """
        Can this bot be pushed closer to the boundary?
        :param action:
        :return:
        """
        drow = 0
        dcol = 0
        if action == ACTIONS.MOVE_NORTH:
            drow = -1
        elif action == ACTIONS.MOVE_SOUTH:
            drow = 1
        elif action == ACTIONS.MOVE_EAST:
            dcol = 1
        elif action == ACTIONS.MOVE_WEST:
            dcol = -1

        centerX = (self.cols - 1) / 2.0
        centerY = (self.rows - 1) / 2.0

        if self.pushable(action):
            pushed_bot = self.bot2 if self.current_player == 1 else self.bot1
            nextBotX = pushed_bot.x + dcol
            nextBotY = pushed_bot.y + drow

            if action == ACTIONS.MOVE_NORTH:
                return nextBotY < centerY
            elif action == ACTIONS.MOVE_SOUTH:
                return nextBotY > centerY
            elif action == ACTIONS.MOVE_EAST:
                return nextBotX < centerX
            elif action == ACTIONS.MOVE_WEST:
                return nextBotX > centerX
        else:
            return False
