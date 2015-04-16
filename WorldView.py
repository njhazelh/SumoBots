
import Tkinter


class WorldView:
    """
    This class isolates the rendering functionality of the game.
    """
    def __init__(self, canvas, cols, rows, canvas_width, canvas_height):
        self.canvas = canvas
        self.cols = cols
        self.rows = rows
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def render(self, world):
        """
        This is the main API with this class.  It renders a world state on
        a previously provided Tkinter canvas.
        """
        self._render_background(world)
        self._render_world(world)

    #=========================================================================
    #
    # Helper Functions
    #
    #=========================================================================

    @property
    def cell_width(self):
        return self.canvas_width / self.cols

    @property
    def cell_height(self):
        return self.canvas_height / self.rows

    def _render_world(self, world):
        oval_x0 = self.cell_width * 6
        oval_y0 = self.cell_height * 6
        oval_x1 = self.canvas_width - oval_x0
        oval_y1 = self.canvas_height - oval_y0
        self.canvas.create_oval(oval_x0, oval_y0, oval_x1, oval_y1, width=5)

        for robot in world.robots:
            self._render_robot(robot)

    def _render_robot(self, robot):
        left = robot.x * self.cell_width
        right = left + self.cell_width
        top = robot.y * self.cell_height
        bottom = top + self.cell_height

        self.canvas.create_rectangle(
            left, top,
            right, bottom,
            fill=robot.color)

    def _render_background(self, world):
        self.canvas.delete(Tkinter.ALL)
        self.canvas.create_rectangle(
            0, 0,
            self.width, self.height,
            fill="white")
