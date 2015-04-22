from Tkinter import *
from datetime import datetime

import SCENES
from Scene import Scene
from models.World import World
from views.WorldView import WorldView


__author__ = 'Nick'


class ArenaScene(Scene):
    """
    ArenaScene is the Scene in which the robots actually fight.
    """

    def prepare(self, kwargs):
        """
        Prepare the initial state of the arena and start the game loop
        :param kwargs: Keyword arguments containing the configuration of the Scene.
            {"config": {1: ROBOT1_TYPE, 2: ROBOT2_TYPE}}
        """
        self.config = kwargs['config']

        self.width = 600
        self.height = 600
        self.turn_start = None
        self.resetting = False
        self.delay_ms = 500

        self.world = World(self.config)

        self.canvas = Canvas(self.master, bg="white", width=self.width, height=self.height)
        self.canvas.pack()
        self.world_view = WorldView(self.world, self.canvas, self.width, self.height)

        # Bind to key events
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key)

        # Start the game loop
        self.render()
        self.after_id = self.after(1000, self.game_loop)

    def game_loop(self):
        """
        Update the world and render.
        The update may not complete due to other
        """
        if self.resetting:
            # Make sure that no old "after" calls run while resetting.
            return

        if self.turn_start is None:
            self.turn_start = datetime.now()

        update_successful = self.update()
        self.render()

        if update_successful:
            # If turn took longer than 1 second, repeat immediately.
            # Else, repeat after 1 second has passed since the start of the turn.
            turn_finish = datetime.now()
            dt = turn_finish - self.turn_start
            self.turn_start = None
            dt_ms = int(dt.total_seconds() * 1000)
            after_ms = max(100, self.delay_ms - dt_ms)
            self.after(after_ms, self.game_loop)
        else:
            # update was not completed. Allow Tk mainloop to get events.
            self.after_id = self.after(0, self.game_loop)

    def render(self):
        """
        Render the world.
        """
        self.world_view.render()

    def update(self):
        """
        Update this Scene
        :return: True if the update completed, else False
        """
        return self.world.update()

    def cleanup(self):
        """
        Destroy the canvas to clean up before destruction.
        """
        self.resetting = True
        self.after_cancel(self.after_id)
        self.canvas.destroy()

    def on_key(self, event):
        """
        Keypress callback
        Need to handle keypress up, down, left, right
        :param event: The Key Event
        """
        if event.keysym == "d":
            self.world.debug = not self.world.debug
        elif event.keysym == "r":
            self.master.set_scene(SCENES.ARENA, config=self.config)
            return
        elif event.keysym == 'minus':
            self.delay_ms = max(0, self.delay_ms - 50)
        elif event.keysym == 'equal':
            self.delay_ms = max(0, self.delay_ms + 50)
        else:
            self.world.key_event = event
        self.world_view.render()
