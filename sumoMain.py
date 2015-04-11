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
   
    w = Scale(root, from_=0, to=100)
    w.pack()

    w = Scale(root, from_=0, to=200, orient=HORIZONTAL)
    w.pack()    
    # Some stuff
    algos = ["Select Algorithm"]
    b = OptionMenu(root, "Select Algorithm", *algos)
    b.pack()

    optionList = ('Select Algorithm', 'plane', 'boat')
    root.v = StringVar()
    root.v.set(optionList[0])
    root.om = OptionMenu(root, root.v, *optionList)
    root.om.pack()
    # Run the Program blocking 
    root.mainloop()  


# Run it!
main()
