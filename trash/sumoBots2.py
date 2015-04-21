#!/usr/bin/python

import time
from Tkinter import *

from Bot import Bot
from trash.World import World
from valueIteration import *
from qLearning import QLearning


def main():
    """
    Main Function
    """
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    # root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.resizable(width=0, height=0)

    cellSize = 40
    rows = cols = 15
    canvasWidth = cols * cellSize
    canvasHeight = rows * cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas

    # Set up canvas data and call init
    canvas.pack()
    canvas.data = {}
    canvas.data["cellSize"] = cellSize
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["rows"] = rows
    canvas.data["cols"] = cols
    canvas.data["reset"] = False

    # this initializes the type of bots that will be used in game play
    initBots(canvas)

    init(canvas)

    canvas.create_text(canvasWidth / 2, (canvasHeight / 2) - 50, text="Loading...", tag="load", fill="red",
                       font=("Helvetica", 32, "bold"))
    canvas.update()

    loadRobotStrategies(canvas)

    canvas.delete("load")
    canvas.update()

    countDown(canvas)

    compGamePlay(canvas)

    # Run the Program blocking
    root.mainloop()


def countDown(canvas):
    """
    Display who's turn it is
    :param canvas: The canvas to render the world on
    """
    cx = canvas.data["canvasWidth"] / 2
    cy = canvas.data["canvasHeight"] / 2

    canvas.create_text(cx, cy - 50, text="3", tag="three", fill="red", font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("three")
    canvas.update()
    canvas.create_text(cx, cy - 50, text="2", tag="two", fill="red", font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("two")
    canvas.update()
    canvas.create_text(cx, cy - 50, text="1", tag="one", fill="red", font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("one")
    canvas.update()
    canvas.create_text(cx, cy - 50, text="Fight!", tag="Fight", fill="red", font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("Fight")
    canvas.update()


def init(canvas):
    """
    Initialize
    :param canvas:
    :return:
    """
    # print usage to terminal window

    bot1Type = canvas.data["bot1Type"]
    bot2Type = canvas.data["bot2Type"]

    # this is to ensure that if there is a human in the game, it always goes first
    if bot1Type == 'h' and bot2Type == 'c':
        bot1InitTurn = True
        bot2InitTurn = False
    elif bot2Type == 'h' and bot1Type == 'c':
        bot1InitTurn = False
        bot2InitTurn = True
    else:
        bot1InitTurn = True
        bot2InitTurn = False

    bot1Strategy = canvas.data["bot1Strategy"]
    bot2Strategy = canvas.data["bot2Strategy"]

    # variables used to develop robot strategies
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    bot1 = Bot(cols / 2 - 3, rows / 2, 1, 1, "blue", canvas, bot1InitTurn, bot1Type, bot1Strategy)
    bot2 = Bot(cols / 2 + 3, rows / 2, 1, 1, "green", canvas, bot2InitTurn, bot2Type, bot2Strategy)
    world = World(rows, cols, bot1, bot2)

    canvas.data["world"] = world
    canvas.data["bot1"] = bot1
    canvas.data["bot2"] = bot2
    canvas.data["sumoGrid"] = world.getSumoGrid()

    # redraw the canvas
    redraw(canvas)

    if canvas.data["reset"] == True:
        canvas.data["reset"] = False
        countDown(canvas)


def compGamePlay(canvas):
    world = canvas.data["world"]
    bot1 = world.bot1
    bot2 = world.bot2
    turns = 500

    # this is only for computer versus computer games
    if bot1.botType == 'c' and bot2.botType == 'c':
        for turn in range(turns):
            if not world.isGameOver():
                # q-learning vs value iteration
                if bot1.strategy == 'q' and bot2.strategy == 'v':
                    if bot1.isTurn():
                        Q = canvas.data["Q"]
                        action = Q.getAction(world, bot1)
                        world.moveBot(bot1, action)
                        Q.update(world, bot1)
                    elif bot2.isTurn():
                        U = canvas.data["U"]
                        world.performBestAction(bot2, U)
                # value iteration versus q-learning
                elif bot1.strategy == 'v' and bot2.strategy == 'q':
                    if bot1.isTurn():
                        U = canvas.data["U"]
                        world.performBestAction(bot1, U)
                    elif bot2.isTurn():
                        Q = canvas.data["Q"]
                        action = Q.getAction(world, bot2)
                        world.moveBot(bot2, action)
                        Q.update(world, bot2)
                # q-learning versus q-learning
                elif bot1.strategy == 'q' and bot2.strategy == 'q':
                    if bot1.isTurn():
                        Q1 = canvas.data["Q1"]
                        action = Q1.getAction(world, bot1)
                        world.moveBot(bot1, action)
                        Q1.update(world, bot1)
                    elif bot2.isTurn():
                        Q2 = canvas.data["Q2"]
                        action = Q2.getAction(world, bot2)
                        world.moveBot(bot2, action)
                        Q2.update(world, bot2)
                # value iteration vs value iteration
                elif bot1.strategy == 'v' and bot2.strategy == 'v':
                    if bot1.isTurn():
                        U = canvas.data["U"]
                        world.performBestAction(bot1, U)
                    elif bot2.isTurn():
                        U = canvas.data["U"]
                        world.performBestAction(bot2, U)

                # toggle turn
                bot1.toggleTurn()
                bot2.toggleTurn()

                # redraw the grid
                redraw(canvas)

                time.sleep(1)

            elif world.isGameOver():
                redraw(canvas)


# Redraw the grid
def redraw(canvas):
    # Clear the Display
    canvas.delete(ALL)

    # Color background
    canvas.create_rectangle(0, 0,
                            canvas.data["canvasWidth"],
                            canvas.data["canvasHeight"],
                            fill="#ccc")

    # Add Title
    canvas.create_text(canvas.data["canvasWidth"] / 2, canvas.data["canvasHeight"] / 8,
                       text="SumoBot Arena",
                       tag="title", fill="#222", font=("Helvetica", 18, "bold"))

    world = canvas.data["world"]
    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]

    # create the sumo ring
    canvas.create_oval(120, 120, 480, 480, width=5, fill="#eee")

    # draw the sumo grid
    drawSumoGrid(canvas)

    # create the sumo ring
    canvas.create_oval(120, 120, 480, 480, width=5)

    # display whose turn it is
    cx = canvas.data["canvasWidth"] - 100
    cy = canvas.data["canvasHeight"] - 10

    if bot1.isTurn():
        canvas.create_text(50, cy - 20,
                           text="Turn: ",
                           fill="#222",
                           font=("Helvetica", 18, "bold"))
        canvas.create_text(140, cy - 20,
                           text="Blue",
                           fill="#22c",
                           font=("Helvetica", 18, "bold"))
    else:
        canvas.create_text(50, cy - 20,
                           text="Turn: ",
                           fill="#222",
                           font=("Helvetica", 18, "bold"))
        canvas.create_text(110, cy - 20,
                           text="Green",
                           fill="#2c2",
                           font=("Helvetica", 18, "bold"))

    # If Game Over write text
    if (world.isGameOver()):
        cx = canvas.data["canvasWidth"] / 2.0
        cy = canvas.data["canvasHeight"] / 2.0
        canvas.create_text(cx, cy,
                           text="Game Over!",
                           font=("Helvetica", 32, "bold"))

    canvas.update()


def drawSumoGrid(canvas):
    """
    Draw the sumo grid
    :param canvas: The canvas to draw on
    """
    sumoGrid = canvas.data["sumoGrid"]
    rows = len(sumoGrid)
    cols = len(sumoGrid[0])

    # Draw the individual row/col cell
    for row in range(rows):
        for col in range(cols):
            drawSumoCell(canvas, sumoGrid, row, col)


def drawSumoCell(canvas, sumoGrid, row, col):
    """
    Draw a single sumo cell
    :param canvas: The canvas to draw on.
    :param sumoGrid: The sumo grid information
    :param row: The row of the cell
    :param col: The column of the cell
    """
    cellSize = canvas.data["cellSize"]
    left = col * cellSize
    right = left + cellSize
    top = row * cellSize
    bottom = top + cellSize

    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]
    world = canvas.data["world"]

    # For debugging: color background and draw cell values.
    if (world.isDebug()):
        if (sumoGrid[row][col] == -9):
            # draw out-of-bounds
            canvas.create_rectangle(left, top, right, bottom, fill="red")
        else:
            # draw in-bounds
            canvas.create_rectangle(left, top, right, bottom)

        # Draw the text in the cell
        canvas.create_text(left + cellSize / 2, top + cellSize / 2,
                           text=str(sumoGrid[row][col]), font=("Helvetica", 14, "bold"))

    if (bot1.is_at(col, row)):
        # Draw the Bot
        canvas.create_rectangle(left, top, right, bottom, fill=bot1.color)
    elif (bot2.is_at(col, row)):
        # Draw the Enemy Bot
        canvas.create_rectangle(left, top, right, bottom, fill=bot2.color)


def initBots(canvas):
    # First determine if the first bot will be a human or a computer
    bot1Type = raw_input("For robot 1 to be human, press h, for robot 1 to be a computer, press c")
    while bot1Type not in ['h', 'c']:
        print 'Please enter either h or c'
        bot1Type = raw_input("For robot 1 to be human, press h, for robot 1 to be a computer, press c")

    # Then, if it is a computer, if it will use valueIteration or q-learning
    if bot1Type == 'c':
        bot1Strategy = raw_input("For robot 1 to use value iteration, press v, for robot 1 to use Q-Learning, press q")
        while bot1Strategy not in ['v', 'q']:
            print 'Please enter either v or q'
            bot1Strategy = raw_input(
                "For robot 1 to use value iteration, press v, for robot 1 to use Q-Learning, press q")

    # Now repeat for the second robot
    bot2Type = raw_input("For robot 2 to be human, press h, for robot 2 to be a computer, press c")
    while bot2Type not in ['h', 'c']:
        print 'Please enter either h or c'
        bot1Type = raw_input("For robot 2 to be human, press h, for robot 2 to be a computer, press c")

    # Then, if it is a computer, if it will use valueIteration or q-learning
    if bot2Type == 'c':
        bot2Strategy = raw_input("For robot 2 to use value iteration, press v, for robot 2 to use Q-Learning, press q")
        while bot2Strategy not in ['v', 'q']:
            print 'Please enter either v or q'
            bot2Strategy = raw_input(
                "For robot 2 to use value iteration, press v, for robot 2 to use Q-Learning, press q")

    # add info to canvas
    canvas.data["bot1Type"] = bot1Type
    canvas.data["bot2Type"] = bot2Type

    if bot1Type == 'c':
        canvas.data["bot1Strategy"] = bot1Strategy
    else:
        canvas.data["bot1Strategy"] = None

    if bot2Type == 'c':
        canvas.data["bot2Strategy"] = bot2Strategy
    else:
        canvas.data["bot2Strategy"] = None


def loadRobotStrategies(canvas):
    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]
    world = canvas.data["world"]

    # computer versus computer
    if bot1.botType == 'c' and bot2.botType == 'c':
        # both value iteration
        if bot1.strategy == 'v' and bot2.strategy == 'v':
            U = runValueIteration(world, bot1, bot2)
            canvas.data["U"] = U
        # both q-learning
        elif bot1.strategy == 'q' and bot2.strategy == 'q':  # only use Q1 and Q2 for 2 q-learning bots. else it is just Q
            Q1 = QLearning(world, bot1, bot2)
            Q2 = QLearning(world, bot1, bot2)
            canvas.data["Q1"] = Q1
            canvas.data["Q2"] = Q2
        # q-learning versus value iteration
        elif bot1.strategy == 'q' and bot2.strategy == 'v':
            Q = QLearning(world, bot1, bot2)
            canvas.data["Q"] = Q
            U = runValueIteration(world, bot1, bot2)
            canvas.data["U"] = U
        # value iteration versus q-learning
        elif bot1.strategy == 'v' and bot2.strategy == 'q':
            U = runValueIteration(world, bot1, bot2)
            canvas.data["U"] = U
            Q = QLearning(world, bot1, bot2)
            canvas.data["Q"] = Q

    # computer versus human
    elif bot1.botType == 'h' and bot2.botType == 'c':
        # bot 2 is value iteration
        if bot2.strategy == 'v':
            U = runValueIteration(world, bot1, bot2)
            canvas.data["U"] = U
        # bot 2 is q-learning
        elif bot2.strategy == 'q':
            Q = QLearning(world, bot1, bot2)
            canvas.data["Q"] = Q
    elif bot1.botType == 'c' and bot2.botType == 'h':
        # bot 1 is value iteration
        if bot1.strategy == 'v':
            U = runValueIteration(world, bot1, bot2)
            canvas.data["U"] = U
        # bot 1 is q-learning
        elif bot1.strategy == 'q':
            Q = QLearning(world, bot1, bot2)
            canvas.data["Q"] = Q

            # human versus human
            # don't load any strategies


# ============================================================================
# Callbacks
# ============================================================================

def mousePressed(event):
    """
    Mouse callback,
    Need to get focus from a mouse click
    :param event: The mouse event
    """
    # get the event
    canvas = event.widget.canvas
    # redraw the grid
    redraw(canvas)


def keyPressed(event):
    """
    Keypress callback
    Need to handle keypress up, down, left, right
    :param event: The Key Event
    """

    # Do not do normal key press operations while robot types and strategies are being determined
    if event.char not in ["e", "r", "d"] and event.keysym not in ["Up", "Down", "Left", "Right"]:
        return

    canvas = event.widget.canvas
    world = canvas.data["world"]
    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]

    # process keys that work even if the game is over
    if (event.char == "e"):
        world.setGameOver(True)
        redraw(canvas)
        return
    elif (event.char == "r"):
        canvas.data["reset"] = True
        init(canvas)
        redraw(canvas)
        return
    elif (event.char == "d"):
        world.toggleDebug()
        redraw(canvas)
        return

        # Process keys that only work if the game is not over and it is the user's turn
        #for bot in (bot1, bot2):
        #    print 'starting for loop'
        # only move the bot if it is a human player and it is it's turn

    if bot1.botType == 'h' and bot1.isTurn():
        userBot = bot1
        otherBot = bot2
    elif bot2.botType == 'h' and bot2.isTurn():
        userBot = bot2
        otherBot = bot1

    # move the user robot
    if not world.isGameOver():
        if (event.keysym == "Up"):
            world.moveBot(userBot, 'North')
        elif (event.keysym == "Down"):
            world.moveBot(userBot, 'South')
        elif (event.keysym == "Left"):
            world.moveBot(userBot, 'West')
        elif (event.keysym == "Right"):
            world.moveBot(userBot, 'East')

        # toggle turns
        userBot.toggleTurn()
        otherBot.toggleTurn()

        # redraw the grid
        redraw(canvas)
        time.sleep(1)

        if not world.isGameOver() and otherBot.isTurn() and otherBot.botType == 'c':
            # is comp bot is value iteration
            if otherBot.strategy == 'v':
                U = canvas.data["U"]
                world.performBestAction(otherBot, U)

                # toggle turn
                bot1.toggleTurn()
                bot2.toggleTurn()

                # redraw the grid
                redraw(canvas)

            # if comp bot is q-learning
            if otherBot.strategy == 'q':
                Q = canvas.data["Q"]
                action = Q.getAction(world, otherBot)
                world.moveBot(otherBot, action)
                Q.update(world, otherBot)

                # toggle turn
                bot1.toggleTurn()
                bot2.toggleTurn()

                # redraw the grid
                redraw(canvas)


if __name__ == "__main__":
    main()
