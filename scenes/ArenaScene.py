from Tkinter import *
from datetime import datetime

from scenes.Scene import Scene
from models.World import World
from views.WorldView import WorldView
import WORLD_STATES

__author__ = 'Nick'


class ArenaScene(Scene):
    def prepare(self, kwargs):
        self.config = kwargs['config']
        print "Config", self.config

        self.width = 600
        self.height = 600
        self.rows = 15
        self.cols = 15

        self.world = World(self.config)

        self.canvas = Canvas(self.master, bg="white", width=self.width, height=self.height)
        self.canvas.pack()
        self.world_view = WorldView(self.world, self.canvas, self.width, self.height)

        # Bind to key events
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key)

        # Start the game loop
        self.after(0, self.game_loop)

    def game_loop(self):
        start_time = datetime.now()
        self.world_view.render()
        self.world.update()

        now = datetime.now()
        dt = now - start_time
        dt_ms = int(dt.total_seconds() * 1000)
        after_ms = max(0, 1000 - dt_ms)
        print "Waiting %d ms" % (after_ms)
        self.after(after_ms, self.game_loop)

    def cleanup(self):
        self.canvas.destroy()

    def on_key(self, event):
        """
        Keypress callback
        Need to handle keypress up, down, left, right
        :param event: The Key Event
        """
        print event.keysym
        if event.keysym == "d":
            self.world.debug = not self.world.debug
        self.world_view.render()

    def __str__(self):
        return "Arena Scene"
