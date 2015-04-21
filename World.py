

class World:
    """
    This class represents the world in which the robots are fighting.
    """

    def __init__(self, rows, cols, bot1, bot2):
        self.game_over = False
        self.debug = False
        self.bot1 = bot1
        self.bot2 = bot2
        self.timer = 400
        self.turn = 1
        self.rows = rows
        self.cols = cols
        self.sumoGrid = []
        self.states = []
        self.ring_radius = 4
        self.gamma = 0.3
        self.delta = 0.1
        self.alpha = 0.5
        self.epsilon = 0.5

        self.initSumoGrid()


    def initSumoGrid(self):
        """
        Initialize the cell values of the sumo Grid.
        Values within bounds are 0.
        Values out of bounds are -9.
        """
        # Initialize 2D array to 0
        for row in range(self.rows):
            self.sumoGrid += [[0] * self.cols]

        # Find the center of the grid
        cx = (self.cols - 1) / 2.0
        cy = (self.rows - 1) / 2.0

        # Set invalid out-of-bounds areas and record in-bound states
        for row in range(self.rows):
            for col in range(self.cols):
                dCenter = ((col - cx) ** 2 + (row - cy) ** 2) ** 0.5

                if round(dCenter) > self.ring_radius:
                    self.sumoGrid[row][col] = -9
                else:
                    stateTuple = (row, col)
                    self.states.append(stateTuple)


    def getSumoGrid(self):
        return self.sumoGrid

    def getNumRows(self):
        return self.rows

    def getNumCols(self):
        return self.cols

    def getBot1(self):
        return self.bot1

    def getBot2(self):
        return self.bot2

    def setGameOver(self, value):
        self.game_over = value
        return self.game_over

    def isGameOver(self):
        return self.game_over

    def toggleDebug(self):
        self.debug = not (self.debug)
        return self.debug

    def isDebug(self):
        return self.debug

    def pushable(self, action):
        drow = 0
        dcol = 0
        if action == "North":
            drow = -1
        elif action == "South":
            drow = 1
        elif action == "East":
            dcol = 1
        elif action == "West":
            dcol = -1

        if self.bot1.isTurn():
            pushing_bot = self.bot1
            pushed_bot = self.bot2
        else:
            pushing_bot = self.bot2
            pushed_bot = self.bot1

        nextY = pushing_bot.yPos + drow
        nextX = pushing_bot.xPos + dcol
        return pushed_bot.is_at(nextX, nextY)

    def can_push_toward_edge(self, action):
        """
        Can this bot be pushed closer to the boundary?
        :param action:
        :return:
        """
        drow = 0
        dcol = 0
        if action == 'North':
            drow = -1
        elif action == 'South':
            drow = 1
        elif action == 'East':
            dcol = 1
        elif action == 'West':
            dcol = -1

        centerX = (self.cols - 1) / 2.0
        centerY = (self.rows - 1) / 2.0

        if self.pushable(action):
            pushed_bot = self.bot2 if self.bot1.isTurn() else self.bot1
            nextBotX = pushed_bot.xPos + dcol
            nextBotY = pushed_bot.yPos + drow

            if action == 'North':
                return nextBotY < centerY
            elif action == 'South':
                return nextBotY > centerY
            elif action == 'East':
                return nextBotX < centerX
            elif action == 'West':
                return nextBotX > centerX
        else:
            return False

    def performBestAction(self, compBot, U):
        """
        Choose and perform the best action.
        :param U: (turn, bot1, bot2) are U key values
        """
        otherBot = None
        turn = 0
        for bot in (self.bot1,self.bot2):
            if bot != compBot:
                otherBot = bot
            if bot == self.bot1:
                turn = 1
            elif bot == self.bot2:
                turn = 2

        compBotState = (compBot.xPos, compBot.yPos)
        otherBotState = (otherBot.xPos, otherBot.yPos)

        maxUtil = 0
        bestAction = None
        for action in compBot.get_legal_actions(compBotState, self):
            nextState = compBot.next_state(compBotState, action)
            nextUtil = U[turn, nextState, otherBotState]
            if nextUtil > maxUtil:
                maxUtil = nextUtil
                bestAction = action
        self.moveBot(compBot,bestAction)

    def moveBot(self, turnBot, action):
        """
        Move the Robot Bot
        Process moving the bot.
        :param bot: the bot whose turn it is, action: The action the bot should perform.
        """
        drow = 0
        dcol = 0


        #if self.bot1.isTurn():
        #    action = self.bot1.randomizeAction(action,self)
        #else:
        #    action = self.bot2.randomizeAction(action,self)
        otherBot = None
        for bot in (self.bot1, self.bot2):
            if bot != turnBot:
                otherBot = bot

        action = turnBot.randomizeAction(action, self)

        if action == 'North':
            drow = -1
        elif action == 'South':
            drow = 1
        elif action == 'East':
            dcol = 1
        elif action == 'West':
            dcol = -1

        #if self.bot1.isTurn():
        nextY = turnBot.yPos + drow
        nextX = turnBot.xPos + dcol

        if nextY == otherBot.yPos and nextX == otherBot.xPos:
            otherBot.xPos += dcol
            otherBot.yPos += drow

            if self.sumoGrid[otherBot.yPos][otherBot.xPos] == -9:
                self.setGameOver(True)

        turnBot.xPos += dcol
        turnBot.yPos += drow

        if self.sumoGrid[turnBot.yPos][turnBot.xPos] == -9:
            self.setGameOver(True)

        #elif self.bot2.isTurn():
        #    nextY = self.bot2.yPos + drow
        #    nextX = self.bot2.xPos + dcol
        #    if nextY == self.bot1.yPos and nextX == self.bot1.xPos:
        #        self.bot1.xPos += dcol
        #        self.bot1.yPos += drow
        #        if self.sumoGrid[self.bot1.yPos][self.bot1.xPos] == -9:
        #            self.setGameOver(True)
        #    self.bot2.xPos += dcol
        #    self.bot2.yPos += drow

        #    if self.sumoGrid[self.bot2.yPos][self.bot2.xPos] == -9:
        #        self.setGameOver(True)
        #    return
