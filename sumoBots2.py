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
    bot1 = Bot(cols/2 - 5, rows/2, 1, 1, "blue", canvas)
    bot2 = Bot(cols/2 + 5, rows/2, 1, 1, "green", canvas)
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
    canvas.data["bot1"] = bot1
    canvas.data["bot2"] = bot2
    canvas.data["turn"] = 1 # Which robot's turn is it now?
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
    
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    bot1 = Bot(cols/2 - 5, rows/2, 1, 1, "blue", canvas)
    bot2 = Bot(cols/2 + 5, rows/2, 1, 1, "green", canvas)
    
    canvas.data["bot1"] = bot1
    canvas.data["bot2"] = bot2
    canvas.data["turn"] = 1
    
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
            elif((col == 6 or col == 23) and ((row >= 6 and row <=10) or (row >= 19 and row <=23))):
                sumoGrid[row][col] = -9
            elif((col == 7 or col == 22) and ((row >= 6 and row <=8) or (row >= 21 and row <=23))):
                sumoGrid[row][col] = -9
            elif((col == 8 or col == 21) and ((row >= 6 and row <=7) or (row >= 22 and row <=23))):
                sumoGrid[row][col] = -9
            elif(((col >= 9 and col <= 10) or (col >= 19 and col <= 20)) and ((row == 6) or (row ==23))):
                sumoGrid[row][col] = -9

    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]
    
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
#	9  = Out-of-bounds
def drawSumoCell(canvas, sumoGrid, row, col):
    #  Get 'global' variables
    cellSize = canvas.data["cellSize"]
    left = col * cellSize
    right = left + cellSize
    top = row * cellSize
    bottom = top + cellSize
    
    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]
    
    if (bot1.isAt(col, row)):
        # Draw the Bot
        canvas.create_rectangle(left, top, right, bottom, fill=bot1.color)
    elif (bot2.isAt(col, row)):
        # Draw the Enemy Bot
        canvas.create_rectangle(left, top, right, bottom, fill=bot2.color)
    # for debugging, draw the number in the cell
    if (canvas.data["inDebugMode"] == True):
        if (sumoGrid[row][col] == -9):
            # draw out-of-bounds
            canvas.create_rectangle(left, top, right, bottom, fill="red")
        
        # Draw the actual grid and values
        canvas.create_rectangle(left, top, right, bottom)
        canvas.create_text(left+cellSize/2,top+cellSize/2, text=str(sumoGrid[row][col]),font=("Helvatica", 14, "bold"))


# Move the Robot-Bot
#  process moving the bot
def moveBot(canvas, action):
    #  Get 'global' variables
    sumoGrid = canvas.data["sumoGrid"]
    bot1 = canvas.data["bot1"]
    bot2 = canvas.data["bot2"]
    
    drow = 0
    dcol = 0
    if action == 'North':
        drow = -1
    elif action == 'South':
        drow = 1
    elif action == 'East':
        dcol = 1
    elif action == 'West':
        dcol = -1
    
    rows = len(sumoGrid)
    cols = len(sumoGrid[0])
    
    if canvas.data["turn"] == 1:
        nextY = bot1.yPos + drow
        nextX = bot1.xPos + dcol
        if nextY == bot2.yPos and nextX == bot2.xPos:
            bot2.xPos += dcol
            bot2.yPos += drow
            if sumoGrid[bot2.yPos][bot2.xPos] == -9:
                gameOver(canvas)
        bot1.xPos += dcol
        bot1.yPos += drow
        if sumoGrid[bot1.yPos][bot1.xPos] == -9:
            gameOver(canvas)

    elif canvas.data["turn"] == 2:
        # Do nothing for now
        return

    canvas.data["bot1"] = bot1
    canvas.data["bot2"] = bot2

# Game Over
#  Process game over event
def gameOver(canvas):
    # Set GameOver attribute
    canvas.data["isGameOver"] = True
    # redraw the grid
    redraw(canvas)

# Bot
class Bot():
    
    def __init__(self, xPos, yPos, power, speed, color, canvas):
        self.xPos = xPos # int for row of bot
        self.yPos = yPos # int for col of bot
        self.power = power # int for how many spaces a bot can push another bot
        self.speed = speed # int for how many spaces a bot can move
        self.color = color
        self.canvas = canvas
    
    def getLegalActions(self):
        rows = self.canvas.data["rows"]
        cols = self.canvas.data["cols"]
        actions = []
        
        # For now just return 1 space to the 'West', 'East', 'North', 'South'
        if xPos + 1 <= cols:
            actions.append['East']
        if xPos - 1 >= 0:
            actions.append['West']
        if yPos + 1 <= rows:
            actions.append['North']
        if yPos - 1 >= 0:
            actions.append['South']
        
        return actions
    
    def move (self, action):
        if action == 'West':
            xPos -= 1
        elif action == 'East':
            xPos += 1
        elif action == 'North':
            yPos += 1
        elif action == 'South':
            yPos -= 1

    # action can be 'West', 'East', 'North', or 'South'
    def isLegalAction (self, action):
        rows = self.canvas.data["rows"]
        cols = self.canvas.data["cols"]
        
        if action == 'West':
            return xPos - 1 >= 0
        elif action == 'East':
            return xPos + 1 <= cols
        elif action == 'North':
            return yPos + 1 <= rows
        elif action == 'South':
            return yPos - 1 >= 0

    def isAt (self, xPos, yPos):
        return self.xPos == xPos and self.yPos == yPos


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
            moveBot(canvas, 'North')
        elif (event.keysym == "Down"):
            moveBot(canvas, 'South')
        elif (event.keysym == "Left"):
            moveBot(canvas, 'West')
        elif (event.keysym == "Right"):
            moveBot(canvas, 'East')
    
    # redraw the grid
    redraw(canvas)
# -------------------- END CALLBACKS --------------------------#

# Run it!
main()
