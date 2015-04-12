from World import World

# Bot
class Bot:
    
    def __init__(self, xPos, yPos, power, speed, color,canvas):
        self.xPos = xPos # int for row of bot
        self.yPos = yPos # int for col of bot
        self.power = power # int for how many spaces a bot can push another bot
        self.speed = speed # int for how many spaces a bot can move
        self.color = color

    def getLegalActions(self, world):
        actions = []
	sumoGrid = world.getSumoGrid()
        
        # For now just return 1 space to the 'West', 'East', 'North', 'South'
        if sumoGrid[self.xPos + 1][self.yPos] != -9:
            actions.append('East')

        if sumoGrid[self.xPos - 1][self.yPos] != -9:
            actions.append('West')

        if sumoGrid[self.xPos][self.yPos - 1] != -9:
            actions.append('North')

        if sumoGrid[self.xPos][self.yPos + 1] != -9:
            actions.append('South')
        
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
