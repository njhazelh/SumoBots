from Tkinter import *

from gui.Scene import Scene

__author__ = 'Nick'

class ArenaScene(Scene):
    def prepare(self, kwargs):
        self.config = kwargs['config']
        print "CONFIG", self.config

        self.width = 600
        self.height = 600
        self.rows = 15
        self.cols = 15

        self.canvas = Canvas(self.master, bg="white", width=self.width, height=self.height)
        self.canvas.pack()

        self.render()

        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key)

        self.after(0, self.game_loop)

    def game_loop(self):
        self.update()
        self.render()
        self.after(1000, self.game_loop)

    def update(self):
        print "UPDATE"

    def render(self):
        self.canvas.create_text(self.width / 2, self.height / 2, text="Robot Arena")

    def cleanup(self):
        self.canvas.destroy()

    def on_key(self, event):
        """
        Keypress callback
        Need to handle keypress up, down, left, right
        :param event: The Key Event
        """
        print event.keysym

    def __str__(self):
        return "ArenaScene"
