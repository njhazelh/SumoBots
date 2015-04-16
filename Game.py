
class Game:
    def __init__(self, world, world_view):
        """
        Initialize the game state
        :param world: The robot world
        :param canvas: The canvas to render the world on
        """
        self.world = world
        self.world_view = world_view

    def start(self):
        """
        Run the game.
        """
        self.prepare()
        self.countdown()
        self.loop()
        self.cleanup()

    def prepare(self):
        """
        Prepare the game's initial state.
        """
        self.world.prepare()
        self.world_view.render(self.world)

    def countdown(self):
        pass

    def loop(self):
        """
        Render and update the game while the game is not over.
        """
        while not self.world.game_over():
            self.render()
            self.update()

    def update(self):
        """
        Update the game state
        """
        self.world.update()

    def render(self):
        """
        Render the game on the canvas
        """
        # something with the canvas
        self.world_view.render(self.world)
