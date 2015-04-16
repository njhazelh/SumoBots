#!/usr/bin/python

import random
import time
from World import World
from Bot import Bot
from SumoArena import SumoArena
from Tkinter import *
from runValueIteration import runValueIteration

# Main function
#  where it all begins
def main():
    """
    Main Function
    """
    # Create the main
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    # set up events
    #root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    root.resizable(width=0, height=0)
    
    cellSize = 20
    rows = cols = 30
    canvasWidth = cols*cellSize
    canvasHeight = rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    
    # Set up canvas data and call init
    canvas.pack()
    canvas.data = { }
    canvas.data["cellSize"] = cellSize
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["rows"] = rows
    canvas.data["cols"] = cols 
    canvas.data["reset"] = False

    init(canvas)

    canvas.create_text(canvasWidth/2, (canvasHeight/2)-50, text="Loading...", tag="load",fill="red",font=("Helvetica", 32, "bold"))
    canvas.update()

    world = canvas.data["world"]
    compBot = canvas.data["compBot"] 
    userBot = canvas.data["userBot"]

    # run value iteration for computer bot
    gamma = .3
    eps = .1
    U = runValueIteration(world, compBot, userBot, gamma, eps)
    canvas.data["U"] = U

    canvas.delete("load")
    canvas.update()

    countDown(canvas)

    # Run the Program blocking
    root.mainloop()

def countDown(canvas):
    # display whose turn it is
    cx = canvas.data["canvasWidth"]/2
    cy = canvas.data["canvasHeight"]/2

    canvas.create_text(cx, cy-50, text="3", tag="three",fill="red",font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("three")
    canvas.update()
    canvas.create_text(cx, cy-50, text="2", tag="two",fill="red",font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("two")
    canvas.update()
    canvas.create_text(cx, cy-50, text="1", tag="one",fill="red",font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("one")
    canvas.update()
    canvas.create_text(cx, cy-50, text="Fight!", tag="Fight",fill="red",font=("Helvetica", 32, "bold"))
    canvas.update()
    time.sleep(1)
    canvas.delete("Fight")
    canvas.update()

# initialize
def init(canvas):
    """
    Initialize
    :param canvas:
    :return:
    """
    # print usage to terminal window
    
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    compBot = Bot(cols/2 - 5, rows/2, 1, 1, "blue", canvas, False)
    userBot = Bot(cols/2 + 5, rows/2, 1, 1, "green", canvas, True)
    world = World(rows,cols,compBot,userBot)
    
    canvas.data["world"] = world
    canvas.data["compBot"] = compBot
    canvas.data["userBot"] = userBot
    canvas.data["sumoGrid"] = world.getSumoGrid()
    
    # redraw the canvas
    redraw(canvas)

    if canvas.data["reset"] == True:
	canvas.data["reset"] = False
	countDown(canvas)

# Redraw the grid
def redraw(canvas):

    # Delete the display

    canvas.delete(ALL) 

    # Add Title
    canvas.create_text(canvas.data["canvasWidth"]/2, canvas.data["canvasHeight"]/8, text="SumoBot Arena", tag="title",fill="black",font=("Helvetica", 18, "bold"))
 
    # unpack world and bot objs
    world = canvas.data["world"]
    compBot = canvas.data["compBot"]
    userBot = canvas.data["userBot"]

    # draw the sumo grid
    drawSumoGrid(canvas)
    # create the sumo ring
    canvas.create_oval(120, 120, 480, 480,width=5)
    
    # display whose turn it is
    cx = canvas.data["canvasWidth"] - 100
    cy = canvas.data["canvasHeight"] - 10

    if (compBot.isTurn()):
	canvas.create_text(50, cy-20, text="Turn: ", fill="black",font=("Helvetica", 18, "bold"))
        canvas.create_text(140, cy-20, text="Computer", fill="blue",font=("Helvetica", 18, "bold"))
    else:
        canvas.create_text(50, cy-20, text="Turn: ", fill="black",font=("Helvetica", 18, "bold"))
        canvas.create_text(110, cy-20, text="User", fill="green",font=("Helvetica", 18, "bold"))

    # If Game Over write text
    if (world.isGameOver()):
        cx = canvas.data["canvasWidth"]/2
        cy = canvas.data["canvasHeight"]/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))

    canvas.update()

# Draw the Sumo Grid
#  This just calls drawSumo cell for every "cell"
def drawSumoGrid(canvas):
    #  Get 'global' variables
    sumoGrid = canvas.data["sumoGrid"]
    rows = len(sumoGrid)
    cols = len(sumoGrid[0])
    
    # Draw the individual row/col cell
    for row in range(rows):
        for col in range(cols):
            drawSumoCell(canvas, sumoGrid, row, col)

# Draw Sumo Cell
#   Draw the Cell, and depending on cell value draw contents
#	9  = Out-of-bounds
def drawSumoCell(canvas, sumoGrid, row, col):
    #  Get 'global' variables
    cellSize = canvas.data["cellSize"]
    left = col * cellSize
    right = left + cellSize
    top = row * cellSize
    bottom = top + cellSize
    
    compBot = canvas.data["compBot"]
    userBot = canvas.data["userBot"]
    world = canvas.data["world"]

    if (compBot.isAt(col, row)):
        # Draw the Bot
        canvas.create_rectangle(left, top, right, bottom, fill=compBot.color)
    elif (userBot.isAt(col, row)):
        # Draw the Enemy Bot
        canvas.create_rectangle(left, top, right, bottom, fill=userBot.color)

    # for debugging, draw the number in the cell
    if (world.isDebug()):
        if (sumoGrid[row][col] == -9):
            # draw out-of-bounds
            canvas.create_rectangle(left, top, right, bottom, fill="red")
        
        # Draw the actual grid and values
        canvas.create_rectangle(left, top, right, bottom)
        canvas.create_text(left+cellSize/2,top+cellSize/2, text=str(sumoGrid[row][col]),font=("Helvatica", 14, "bold"))

# -------------------- CALLBACKS ------------------------------#
# Mouse Callback
#   Need to get focus from a Mouse click
def mousePressed(event):
    # get the event
    canvas = event.widget.canvas
    # redraw the grid
    redraw(canvas)

# Keypress Callback
#   Need to handle keypress up,down,left,right
def keyPressed(event):
    # get the event
    canvas = event.widget.canvas
    world = canvas.data["world"]
    compBot = canvas.data["compBot"]
    userBot = canvas.data["userBot"]

    # process keys that work even if the game is over
    if (event.char == "q"):
        world.setGameOver(True)
    elif (event.char == "r"):
	canvas.data["reset"] = True
        init(canvas)
    elif (event.char == "d"):
        world.toggleDebug()

    # Process keys that only work if the game is not over
    if (world.isGameOver() == False) and (userBot.isTurn()):
        if (event.keysym == "Up"):
            world.moveBot('North')
        elif (event.keysym == "Down"):
            world.moveBot('South')
        elif (event.keysym == "Left"):
            world.moveBot('West')
        elif (event.keysym == "Right"):
            world.moveBot('East')

        # toggle turn 
        compBot.toggleTurn()
        userBot.toggleTurn()

        # redraw the grid
        redraw(canvas)

	time.sleep(1)

        if (world.isGameOver() == False) and (compBot.isTurn()):
            U = canvas.data["U"]
            world.performBestAction(U)
  
            # toggle turn 
            compBot.toggleTurn()
            userBot.toggleTurn()

            # redraw the grid
            redraw(canvas)

        # need to change this to a robot.getBestAction method
        #world.moveBot('East')
        



# -------------------- END CALLBACKS --------------------------#

# Run it!
main()
