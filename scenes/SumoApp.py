from scenes import SCENES
from scenes.ArenaScene import  ArenaScene
from scenes.RobotConfigScene import RobotConfigScene
from scenes.TitleScene import TitleScene

__author__ = 'Nick'

from Tkinter import *

class SumoApp(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.scene = None
        self.set_scene(SCENES.TITLE)

    def set_scene(self, scene, **kwargs):
        if self.scene is not None:
            print "Destroying %s" % (self.scene)
            self.scene.destroy()
            self.pack()
        if scene == SCENES.TITLE:
            self.scene = TitleScene(self)
        elif scene == SCENES.ROBOT_1:
            self.scene = RobotConfigScene(self, robot=1, config=None)
        elif scene == SCENES.ROBOT_2:
            self.scene = RobotConfigScene(self, robot=2, config=kwargs['config'])
        elif scene == SCENES.ARENA:
            self.scene = ArenaScene(self, config=kwargs['config'])
        else:
            self.scene = None

def main():
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    root.resizable(width=0, height=0)
    app = SumoApp(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
