


# add to sumoBots2
	Usorted = sorted(U, key=U.get)
	print Usorted

	    U = runValueIteration(world, compBot, userBot, gamma, eps)
    canvas.data["U"] = U
    
    # redraw the canvas
    redraw(canvas)
@@ -185,7 +186,8 @@ def keyPressed(event):
        redraw(canvas)

        if (world.isGameOver() == False) and (compBot.isTurn()):
            world.moveBot('East')
            U = canvas.data["U"]
            world.performBestAction(U)


    canvas.data["U"] = U