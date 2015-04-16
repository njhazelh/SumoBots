
class Robot:
    def __init__(self, strategy, color):
        self.strategy = strategy
        self.color = color
        self.x = 0
        self.y = 0

    def prepare(self, world):
        self.strategy.prepare(world)

    def update(self, world):
        pass
