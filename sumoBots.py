# Tim T
# Robot-Sumo

import random
from Tkinter import *

# Main function
#  where it all begins
def main():
    # Create the main
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    # set up events
    root.bind("<Button-1>", mousePressed)
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
    init(canvas)

    # Run the Program blocking
    root.mainloop()

# initialize
def init(canvas):
    # print usage to terminal window
    usage()
    #initialize global variables.
    canvas.data["isGameOver"] = False
    canvas.data["inDebugMode"] = False

    # load the Sumo Grid
    initSumoGrid(canvas)

    # redraw the canvas
    redraw(canvas)

def usage():
    print "Robot-Sumo, FIGHT!"
    print "Use the arrow keys to move the blue SumoBot."
    print "Stay with the black ring, and push the green SumoBot out."
    print "Press 'd' for debug mode."
    print "Press 'r' to restart."

# Initialize Sumo Grid
#  set the initial values for cells 9 = out-of-bounds and
#  is what is really being set here
def initSumoGrid(canvas):
    #  Get 'global' variables
    sumoGrid = [ ]
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]

    # Initialize 2D array to 0
    for row in range(rows):
	sumoGrid += [[0] * cols]

    # Set invalid out-of-bounds areas
    for row in range(rows):
	for col in range(cols):
	    if((col <= 5 or col >=24) or
		(row <=5 or row >=24)):
		sumoGrid[row][col] = -9
	    elif((col == 6 or col == 23) and
		((row >= 6 and row <=10) or
		 (row >= 19 and row <=23))):
		sumoGrid[row][col] = -9
	    elif((col == 7 or col == 22) and
		((row >= 6 and row <=8) or
		 (row >= 21 and row <=23))):
		sumoGrid[row][col] = -9
	    elif((col == 8 or col == 21) and
		((row >= 6 and row <=7) or
		 (row >= 22 and row <=23))):
		sumoGrid[row][col] = -9
	    elif(((col >= 9 and col <= 10) or
		  (col >= 19 and col <= 20)) and
		((row == 6) or (row ==23))):
		sumoGrid[row][col] = -9

    # Initialize Bot #1 position
    sumoGrid[rows/2][cols/2 - 5] = 1
    canvas.data["bot1Row"] = rows/2
    canvas.data["bot1Col"] = cols/2 - 5
    # Initialize Bot #2 position
    sumoGrid[rows/2][cols/2 + 5] = -1

    # Store the sumoGrid information
    canvas.data["sumoGrid"] = sumoGrid

# Redraw the grid
def redraw(canvas):
    # Delete the display
    canvas.delete(ALL)
    # draw the sumo grid
    drawSumoGrid(canvas)
    # create the sumo ring
    canvas.create_oval(120, 120, 480, 480,width=5)

    # If Game Over write text
    if (canvas.data["isGameOver"] == True):
        cx = canvas.data["canvasWidth"]/2
        cy = canvas.data["canvasHeight"]/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))

# Draw the Sumo Grid
#  This just calls drawSumo cell for every "cell"
def drawSumoGrid(canvas):
    #  Get 'global' variables
    sumoGrid = canvas.data["sumoGrid"]
    sumoGrid = canvas.data["sumoGrid"]
    rows = len(sumoGrid)
    cols = len(sumoGrid[0])

    # Draw the individual row/col cell
    for row in range(rows):
        for col in range(cols):
            drawSumoCell(canvas, sumoGrid, row, col)

# Draw Sumo Cell
#   Draw the Cell, and depending on cell value draw contents
#	1  = Bot #1
#	-1 = Bot #2
#	9  = Out-of-bounds
def drawSumoCell(canvas, sumoGrid, row, col):
    #  Get 'global' variables
    cellSize = canvas.data["cellSize"]
    left = col * cellSize
    right = left + cellSize
    top = row * cellSize
    bottom = top + cellSize

    if (sumoGrid[row][col] == 1):
        # Draw the Bot
        canvas.create_rectangle(left, top, right, bottom, fill="blue")
    elif (sumoGrid[row][col] == -1):
        # Draw the Enemy Bot
        canvas.create_rectangle(left, top, right, bottom, fill="green")
    # for debugging, draw the number in the cell
    if (canvas.data["inDebugMode"] == True):
	if (sumoGrid[row][col] == -9):
      	    # draw out-of-bounds
            canvas.create_rectangle(left, top, right, bottom, fill="red")

        # Draw the actual grid and values
	canvas.create_rectangle(left, top, right, bottom)
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(sumoGrid[row][col]),font=("Helvatica", 14, "bold"))

# Move the Robot-Bot
#  process moving the bot
def moveBot(canvas, drow, dcol):
    #  Get 'global' variables
    sumoGrid = canvas.data["sumoGrid"]
    bot1Row = canvas.data["bot1Row"]
    bot1Col = canvas.data["bot1Col"]

    rows = len(sumoGrid)
    cols = len(sumoGrid[0])

    newHeadRow = bot1Row + drow
    newHeadCol = bot1Col + dcol
    prevValue = sumoGrid[newHeadRow][newHeadCol]

    # Move to new space
    sumoGrid[newHeadRow][newHeadCol] = 1 + sumoGrid[bot1Row][bot1Col];
    canvas.data["bot1Row"] = newHeadRow
    canvas.data["bot1Col"] = newHeadCol

    # Remove bot from old space
    for row in range(rows):
        for col in range(cols):
            if (sumoGrid[row][col] > 0):
                sumoGrid[row][col] -= 1

    # Is it game over, or did we hit the other bot?
    if (prevValue == -9):
        gameOver(canvas)
    elif (prevValue == -1):
        botHit(canvas)

# Game Over
#  Process game over event
def gameOver(canvas):
    # Set GameOver attribute
    canvas.data["isGameOver"] = True
    # redraw the grid
    redraw(canvas)

# Bot Hit
# When bots collide we need to do some processing
def botHit(canvas):
    #  Get 'global' variables
    sumoGrid = canvas.data["sumoGrid"]
    rows = len(sumoGrid)
    cols = len(sumoGrid[0])

    # for now just randomly move bot #2 to a different
    # location
    # Pick a row/col that isn't occupied or out-of-bounds
    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if (sumoGrid[row][col] == 0):
            break

    # set the grid
    sumoGrid[row][col] = -1

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

    # process keys that work even if the game is over
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        init(canvas)
    elif (event.char == "d"):
        canvas.data["inDebugMode"] = not canvas.data["inDebugMode"]

    # Process keys that only work if the game is not over
    if (canvas.data["isGameOver"] == False):
        if (event.keysym == "Up"):
            moveBot(canvas, -1, 0)
        elif (event.keysym == "Down"):
            moveBot(canvas, +1, 0)
        elif (event.keysym == "Left"):
            moveBot(canvas, 0,-1)
        elif (event.keysym == "Right"):
            moveBot(canvas, 0,+1)

    # redraw the grid
    redraw(canvas)
# -------------------- END CALLBACKS --------------------------#

if __name__ == "__main__":
    main()
