from models.Robot import Robot
import WORLD_STATES
from strategies import STRATEGIES

__author__ = 'Nick'

class World:
    def __init__(self, config):
        self.debug = False
        self.cols = 15
        self.rows = 15
        self.ring_radius = 4
        self.states = []
        self.sumo_grid = []
        self.game_over = False
        self.state = WORLD_STATES.COUNT_DOWN
        self.count = 3

        self.bot1 = Robot(self.cols / 2 - 3, self.rows / 2, self, "#a00", type=config[1])
        self.bot2 = Robot(self.cols / 2 + 3, self.rows / 2, self, "#0a0", type=config[2])

        if config[1] == STRATEGIES.HUMAN or config[2] != STRATEGIES.HUMAN:
            self.current_player = 1
        else:
            self.current_player = 2

        self.init_grid()


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
                else:
                    stateTuple = (row, col)
                    self.states.append(stateTuple)

    def update(self):
        print "UPDATE WORLD"
        if self.state == WORLD_STATES.COUNT_DOWN:
            self.count -= 1
            if self.count == -1:
                self.state = WORLD_STATES.PLAYING
        elif self.state == WORLD_STATES.PLAYING:
            if self.current_player == 1:
                self.bot1.update()
                self.current_player = 2
            else:
                self.bot2.update()
                self.current_player = 1
        elif self.state == WORLD_STATES.GAME_OVER:
            pass
        else:
            raise Exception("World in an unknown state: %s" % (self.state))
