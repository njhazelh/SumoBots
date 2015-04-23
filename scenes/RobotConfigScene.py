from Tkinter import *

from scenes import SCENES
from scenes.Scene import Scene
from strategies import STRATEGIES


__author__ = 'Nick'


class RobotConfigScene(Scene):
    def prepare(self, kwargs):
        self.width = 600
        self.height = 600

        self.robot = kwargs['robot']
        if kwargs['config'] is None:
            self.config = {}
        else:
            self.config = kwargs['config']

        self.canvas = Canvas(self.master, bg="white", width=self.width, height=self.height)
        self.canvas.pack()
        self.render()

        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key)

    def render(self):
        self.canvas.create_text(self.width / 2, 240,
                                text="Press key to choose robot %d strategy." % (self.robot),
                                font=("Helvetica", 12, "bold"))
        self.canvas.create_text(self.width / 2, 300,
                                text="h: Human Control")
        self.canvas.create_text(self.width / 2, 340,
                                text="v: Value Iteration")
        self.canvas.create_text(self.width / 2, 380,
                                text="q: Q-Learning")

    def on_key(self, key):
        if key.keysym not in ["q", "h", "v"]:
            return

        if key.keysym == "q":
            self.config[self.robot] = STRATEGIES.Q_LEARNING
        elif key.keysym == "h":
            self.config[self.robot] = STRATEGIES.HUMAN
        elif key.keysym == "v":
            self.config[self.robot] = STRATEGIES.VALUE_ITERATION

        self.master.next_scene(config=self.config)

    def cleanup(self):
        self.canvas.destroy()

    def __str__(self):
        return "Robot %d config scene" % (self.robot)
