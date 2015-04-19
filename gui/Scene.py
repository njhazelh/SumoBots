__author__ = 'Nick'

from Tkinter import *

class Scene(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)
        self.master = master
        self.prepare(kwargs)

    def prepare(self, kwargs):
        pass

    def render(self):
        pass

    def cleanup(self):
        pass

    def destroy(self):
        self.cleanup()
        Frame.destroy(self)
