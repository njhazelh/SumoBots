from gui import SCENES
from gui.Scene import Scene

__author__ = 'Nick'

from Tkinter import *

class TitleScene(Scene):
    def prepare(self, kwargs):
        self.width = 600
        self.height = 600
        self.canvas = Canvas(self.master, bg="white", width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_enter)
        self.render()

    def on_enter(self, event):
        if event.keysym == "Return":
            self.master.set_scene(SCENES.ROBOT_1)

    def render(self):
        self.canvas.create_text(self.width / 2,
                                self.height / 2 - 50,
                                text="SumoBots!",
                                font=("Helvetica", 32, "bold"),
                                fill="red")
        self.canvas.create_text(self.width / 2,
                                self.height / 2 + 50,
                                text="Click <Enter> to begin",
                                font=("Helvetica", 12, "normal"))

    def cleanup(self):
        self.canvas.destroy()

    def __str__(self):
        return "Title Scene"
