from scenes import SCENES
from scenes.ArenaScene import ArenaScene
from scenes.RobotConfigScene import RobotConfigScene
from scenes.TitleScene import TitleScene

__author__ = 'Nick'

from Tkinter import *


class SumoApp(Frame):
    def __init__(self, master, robot1, robot2):
        Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.scene = None
        self.config = {
            1: robot1,
            2: robot2
        }
        self.set_scene(SCENES.TITLE)

    def next_scene(self, **kwargs):


        if self.scene is None:
            self.set_scene(SCENES.TITLE, **kwargs)
        elif self.config[1] is None:
            self.set_scene(SCENES.ROBOT_1, **kwargs)
        elif self.config[2] is None:
            self.set_scene(SCENES.ROBOT_2, **kwargs)
        else:
            self.set_scene(SCENES.ARENA, **kwargs)

    def set_scene(self, scene, **kwargs):
        if self.scene is not None:
            self.scene.destroy()
            self.pack()

        if kwargs.get("config", None) is not None:
            self.config = kwargs.get("config", self.config)

        if scene == SCENES.TITLE:
            self.scene = TitleScene(self)
        elif scene == SCENES.ROBOT_1 and self.config[1] is None:
            self.scene = RobotConfigScene(self, robot=1, config=self.config)
        elif scene == SCENES.ROBOT_2 and self.config[2] is None:
            self.scene = RobotConfigScene(self, robot=2, config=self.config)
        elif scene == SCENES.ARENA:
            self.scene = ArenaScene(self, config=self.config)
        else:
            self.scene = None
