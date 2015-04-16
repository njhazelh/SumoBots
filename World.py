
class World:
    def __init__(self, robots, columns, rows):
        self.robots = robots
        self.columns = columns
        self.rows = rows

    def prepare(self):
        for r in self.robots:
            r.prepare(self)

    def update(self):
        for r in self.robots:
            r.update(self)

    def game_over(self):
        pass
