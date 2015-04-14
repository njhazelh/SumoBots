from Tkinter import *

from Bot import Bot
from World import World


class SumoArena:
    def __init__(self, world):
        self.world = world
        rows = world.getNumRows()
        cols = world.getNumCols()

        self.sumoArena = Tk()
        self.sumoArena.title("Robot-Sumo Arena [by Team Wall-E]")
        self.sumoArena.bind("<Button-1>", self.mousePressed)
        self.sumoArena.bind("<Key>", self.keyPressed)
        self.sumoArena.resizable(width=0, height=0)

        self.cellSize = 20
        canvasWidth = cols * self.cellSize
        canvasHeight = rows * self.cellSize

        self.sumoArena.canvas = Canvas(self.sumoArena, width=canvasWidth, height=canvasHeight)
        self.sumoArena.canvas.pack()

        # redraw the canvas
        self.redraw(world)

        # Run the Program blocking
        self.sumoArena.mainloop()

    def redraw(self, world):
        """
        Redraw the grid
        :param world:
        :return:
        """
        self.world = world
        # Delete the display
        self.sumoArena.canvas.delete(ALL)
        # draw the sumo grid
        self.drawSumoGrid(world)
        # create the sumo ring
        self.sumoArena.canvas.create_oval(120, 120, 480, 480, width=5)

        # If Game Over write text
        if (world.isGameOver()):
            self.sumoArena.canvas.create_text(300, 300, text="Game Over!", font=("Helvetica", 32, "bold"))


    def drawSumoGrid(self, world):
        """
        Draw the Sumo Grid
        This just calls drawSumo cell for every "cell"
        :param world:
        :return:
        """
        rows = world.getNumRows()
        cols = world.getNumCols()

        # Draw the individual row/col cell
        for row in range(rows):
            for col in range(cols):
                self.drawSumoCell(world, row, col)


    def drawSumoCell(self, world, row, col):
        """
        Draw Sumo Cell
        Draw the Cell, and depending on cell value draw contents
        9  = Out-of-bounds

        :param world:
        :param row:
        :param col:
        :return:
        """
        left = col * self.cellSize
        right = left + self.cellSize
        top = row * self.cellSize
        bottom = top + self.cellSize

        sumoGrid = self.world.getSumoGrid()
        bot1 = self.world.getBot1()
        bot2 = self.world.getBot2()

        if (bot1.isAt(col, row)):
            # Draw the Bot
            self.sumoArena.canvas.create_rectangle(left, top, right, bottom, fill=bot1.color)
        elif (bot2.isAt(col, row)):
            # Draw the Enemy Bot
            self.sumoArena.canvas.create_rectangle(left, top, right, bottom, fill=bot2.color)

        # for debugging, draw the number in the cell
        if (self.world.isDebug()):
            if (sumoGrid[row][col] == -9):
                # draw out-of-bounds
                self.sumoArena.canvas.create_rectangle(left, top, right, bottom, fill="red")

            # Draw the actual grid and values
            self.sumoArena.canvas.create_rectangle(left, top, right, bottom)
            self.sumoArena.canvas.create_text(left + self.cellSize / 2, top + self.cellSize / 2,
                                              text=str(sumoGrid[row][col]), font=("Helvetica", 14, "bold"))

    # -------------------- CALLBACKS ------------------------------#

    def mousePressed(self, event):
        """
        Mouse Callback
        Need to get focus from a Mouse click
        """
        # redraw the grid
        self.redraw(self.world)


    def keyPressed(self, event):
        """
        Keypress Callback
        Need to handle keypress up,down,left,right
        :param event:
        :return:
        """
        # process keys that work even if the game is over
        if (event.char == "q"):
            self.world.setGameOver(True)
        elif (event.char == "x"):
            self.sumoArena.quit()
        elif (event.char == "r"):
            rows = cols = 30
            canvas = 1
            bot1 = Bot(cols / 2 - 5, rows / 2, 1, 1, "blue", canvas)
            bot2 = Bot(cols / 2 + 5, rows / 2, 1, 1, "green", canvas)
            world = World(rows, cols, bot1, bot2)
            self.redraw(world)
        elif (event.char == "d"):
            self.world.toggleDebug()

        # Process keys that only work if the game is not over
        if (self.world.isGameOver() == False):
            if (event.keysym == "Up"):
                self.world.moveBot('North')
            elif (event.keysym == "Down"):
                self.world.moveBot('South')
            elif (event.keysym == "Left"):
                self.world.moveBot('West')
            elif (event.keysym == "Right"):
                self.world.moveBot('East')

        # redraw the grid
        self.redraw(self.world)

# -------------------- END CALLBACKS --------------------------#

