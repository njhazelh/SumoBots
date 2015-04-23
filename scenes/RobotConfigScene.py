from Tkinter import *

from scenes import SCENES
from scenes.Scene import Scene
from strategies import STRATEGIES

class RobotConfigScene(Scene):
    def prepare(self, kwargs):
        self.width = 600
        self.height = 600

        self.robot = kwargs['robot']
        if kwargs['config'] is None:
            self.config = {}
        else:
            self.config = kwargs['config']

        self.canvas = Canvas(self.master, bg="#555", width=self.width, height=self.height)
        self.canvas.pack()
        self.render()

        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key)

    def render(self):
        self.canvas.create_text(self.width / 2, 240,
                                text="Robot %s: Press key to select strategy." % (self.robot),
                                fill="#afa",
                                font=("Helvetica", 16, "bold"))

        self.canvas.create_text(self.width / 2, 300,
                                text="h: Human Control",
                                fill="#aaa",
                                font=("Helvetica", 14, "normal"))
        self.canvas.create_text(self.width / 2, 340,
                                text="r: Random",
                                fill="#aaa",
                                font=("Helvetica", 14, "normal"))
        self.canvas.create_text(self.width / 2, 380,
                                text="v: Value Iteration",
                                fill="#aaa",
                                font=("Helvetica", 14, "normal"))
        self.canvas.create_text(self.width / 2, 420,
                                text="q: Q-Learning",
                                fill="#aaa",
                                font=("Helvetica", 14, "normal"))

    def on_key(self, key):
        if key.keysym not in ["q", "h", "r", "v"]:
            return
        self.config[self.robot] = STRATEGIES.key_to_strategy(key.keysym)
        self.master.next_scene(config=self.config)

    def cleanup(self):
        self.canvas.destroy()

    def __str__(self):
        return "Robot %d config scene" % (self.robot)
