# Bot
class Bot:
    
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
