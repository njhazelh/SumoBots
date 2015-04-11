class Robot:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.strategy = None

  def set_strategy(self, strategy):
    self.strategy = strategy

  def choose_action(self, world):
    self.strategy.choose_action(world)

