from World import World

# Bot
class Bot:

    def __init__(self, xPos, yPos, power, speed, color, canvas, turn):
        self.xPos = xPos # int for row of bot
        self.yPos = yPos # int for col of bot
        self.power = power # int for how many spaces a bot can push another bot
        self.speed = speed # int for how many spaces a bot can move
        self.color = color
        self.turn = turn
        self.failProb = .2

    def getLegalActions(self, state, world):
        actions = []
        sumoGrid = world.getSumoGrid()

        # For now just return 1 space to the 'West', 'East', 'North', 'South'
        if sumoGrid[state[0] + 1][state[1]] != -9:
            actions.append('East')

        if sumoGrid[state[0] - 1][state[1]] != -9:
            actions.append('West')

        if sumoGrid[state[0]][state[1] + 1] != -9:
            actions.append('North')

        if sumoGrid[state[0]][state[1] - 1] != -9:
            actions.append('South')

        return actions

    def getAllActions(self, world):
        allActions = {}
        for state in world.getStates():
            allActions[state] = self.getLegalActions(state, world)
        return allActions

    def getTransitionModel(self, world):
        transModel = {}
        for state in world.getStates():
            legalActions = self.getLegalActions(state, world)
            numActions = len(legalActions)
            pWrongAction = self.failProb/(numActions - 1)   # divide the probability of failure equally among the wrong actions
            for actionAttempt in legalActions:
                transModel[state, actionAttempt] = {}
                for actionOccur in legalActions:
                    nextState = self.nextState(state, actionOccur)
                    if actionAttempt == actionOccur:
                        transModel[(state, actionAttempt)][nextState] = 1 - self.failProb # prob of performing the correct action
                    else:
                        transModel[(state, actionAttempt)][nextState] = pWrongAction
        return transModel

    def state(self):
        return(self.xPos,self.yPos)

    def nextState(self, state, action):

        xPos = state[0]
        yPos = state[1]
        if action == 'West':
            xPos = state[0] - 1
        elif action == 'East':
            xPos = state[0] + 1
        elif action == 'North':
            yPos = state[1] + 1
        elif action == 'South':
            yPos = state[1] - 1

        return (xPos, yPos)

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

    def isTurn(self):
        return self.turn

    def toggleTurn(self):
        self.turn = not(self.turn)

