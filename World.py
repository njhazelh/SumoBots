class World:
  """
  This class represents the world in which the robots are fighting.
  """
  def __init__(self, rows, cols, bot1, bot2):
    self.gameOver = False
    self.debug    = False
    self.bot1	  = bot1
    self.bot2	  = bot2
    self.timer    = 400
    self.turn	  = 1
    self.rows	  = rows
    self.cols     = cols
    self.sumoGrid = []
    self.states   = []

    self.initSumoGrid()

  # Initialize Sumo Grid
  #  set the initial values for cells 9 = out-of-bounds and
  #  is what is really being set here
  def initSumoGrid(self):
    # Initialize 2D array to 0
    for row in range(self.rows):
        self.sumoGrid += [[0] * self.cols]
    
    # Set invalid out-of-bounds areas
    for row in range(self.rows):
        for col in range(self.cols):
            if((col <= 5 or col >=24) or
               (row <=5 or row >=24)):
                self.sumoGrid[row][col] = -9
            elif((col == 6 or col == 23) and 
		((row >= 6 and row <=10) or (row >= 19 and row <=23))):
                self.sumoGrid[row][col] = -9
            elif((col == 7 or col == 22) and 
		((row >= 6 and row <=8) or (row >= 21 and row <=23))):
                self.sumoGrid[row][col] = -9
            elif((col == 8 or col == 21) and 
		((row >= 6 and row <=7) or (row >= 22 and row <=23))):
                self.sumoGrid[row][col] = -9
            elif(((col >= 9 and col <= 10) or (col >= 19 and col <= 20)) and 
		((row == 6) or (row ==23))):
                self.sumoGrid[row][col] = -9
	    else:
		stateTuple = (row,col)
		self.states.append(stateTuple)

  def getStates(self):
    # get a list of all valid states, where a state is a (x,y) position tuple

      states = []
      for row in range(self.rows):
          for col in range(self.cols):
              states.append((row, col))

      return states

  def getSumoGrid(self):
    return self.sumoGrid

  def tick(self):
    """
    A Unit of time passes
    """
    pass

  def states(self):
    return self.states

  def render(self):
    """
    Returns a rendering of the world that the GUI can show.
    """
    pass

  def getNumRows(self):
    return self.rows

  def getNumCols(self):
    return self.cols

  def getBot1(self):
    return self.bot1

  def getBot2(self):
    return self.bot2

  def setGameOver(self,value):
    self.gameOver = value
    return self.gameOver

  def isGameOver(self):
    return self.gameOver

  def toggleDebug(self):
    self.debug = not (self.debug)
    return self.debug

  def isDebug(self):
    return self.debug

  # Move the Robot-Bot
  #  process moving the bot
  def moveBot(self, action):
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
    
    rows = len(self.sumoGrid)
    cols = len(self.sumoGrid[0])
    
    if self.turn == 1:
        nextY = self.bot1.yPos + drow
        nextX = self.bot1.xPos + dcol
        if nextY == self.bot2.yPos and nextX == self.bot2.xPos:
            self.bot2.xPos += dcol
            self.bot2.yPos += drow
            if self.sumoGrid[self.bot2.yPos][self.bot2.xPos] == -9:
                self.setGameOver(True)
        self.bot1.xPos += dcol
        self.bot1.yPos += drow

        if self.sumoGrid[self.bot1.yPos][self.bot1.xPos] == -9:
            self.setGameOver(True)

    elif self.turn == 2:
        # Do nothing for now
        return
