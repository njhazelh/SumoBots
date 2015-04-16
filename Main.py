
import Tkinter

import Robots
from World import World
from Game import Game
from WorldView import WorldView


def main():
    # Create Robots. This can be modified later.
    robot1 = Robots.HumanRobot("green")
    robot2 = Robots.HumanRobot("blue")
    robots = [robot1, robot2]

    # Define Arena Boundaries
    cols = 30
    rows = 30
    canvas_width = 600  # pixels
    canvas_height = 600  # pixels

    # Create Tkinter Object
    root = Tkinter.Tk()
    root.title("Robot-Sumo Arena: Team Wall-E")
    root.resizable(width=0, height=0)
    canvas = Tkinter.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Create World State and View
    world = World(robots, cols, rows)
    world_view = WorldView(canvas, cols, rows, canvas_width, canvas_height)

    # Create and run game
    game = Game(world, world_view)
    game.start()

    root.mainloop()

if __name__ == "__main__":
    main()
