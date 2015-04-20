__author__ = 'Nick'

from Tkinter import *

class Scene(Frame):
    """
    A Scene represents a single unit page in a GUI.
    For example, the title page and a ranking page would be different scenes.
    Which scene is shown in the GUI is controlled by the application Frame.
    Scenes can access this Frame through 'self.master' to request scene changes.
    """
    def __init__(self, master, **kwargs):
        """
        Handle initialization of the Scene with the master.
        Scenes that implement this interfaces should override prepare rather than
        __init__.  This is because otherwise they would overwrite glue code.

        :param master: The containing Tkinter Frame.
        :param kwargs: A dict of keyword args that are specific to each Scene.
        """
        Frame.__init__(self, master)
        self.master = master
        self.prepare(kwargs)

    def prepare(self, kwargs):
        """
        Called by __init__ to initialize the scene.
        :param kwargs: A dict of keyword arguments that are specific to each Scene.
        """
        pass

    def cleanup(self):
        """
        Clean up elements such as canvases used within the scene.
        Called by destroy.
        """
        pass

    def destroy(self):
        """
        Destroy this frame, and call cleanup.
        Subclasses should not override this.
        """
        self.cleanup()
        Frame.destroy(self)
