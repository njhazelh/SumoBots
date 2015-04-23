from scenes import SCENES
from scenes.Scene import Scene

__author__ = 'Nick'

from Tkinter import *


class TitleScene(Scene):
    def prepare(self, kwargs):
        self.width = 600
        self.height = 600
        self.canvas = Canvas(self.master, bg="#555", width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_enter)
        self.render()

    def on_enter(self, event):
        if event.keysym == "Return":
            self.master.next_scene()

    def render(self):
        self.canvas.create_text(self.width / 2,
                                self.height / 2 - 50,
                                text="SumoBots!",
                                font=("Helvetica", 40, "bold"),
                                fill="#afa")
        self.canvas.create_text(self.width / 2,
                                self.height / 2 + 30,
                                fill="#ccc",
                                text="Click <Enter> to begin",
                                font=("Helvetica", 14, "normal"))

    def cleanup(self):
        self.canvas.destroy()

    def __str__(self):
        return "Title Scene"
