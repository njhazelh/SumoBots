class World:
  """
  This class represents the world in which the robots are fighting.
  """
  def __init__(self, bot1, bot2):
    self.gameOver = False
    self.debug    = False
    self.bot1	  = bot1
    self.bot2	  = bot2
    self.timer    = 400

  def tick(self):
    """
    A Unit of time passes
    """
    pass

  def render(self):
    """
    Returns a rendering of the world that the GUI can show.
    """
    pass

  def getBot1(self):
    return self.bot1

  def getBot2(self):
    return self.bot2

  def setGameOver(self,value):
    self.gameOver = value
    return self.gameOver

  def isGameOver(self):
    return self.gameOver

  def setDebug(self,value):
    self.debug = value
    return self.debugls

  def isDebug(self):
    return self.debug
