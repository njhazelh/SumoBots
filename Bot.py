# Bot
import random

class Bot:
    def __init__(self, xPos, yPos, power, speed, color, canvas, turn, botType, strategy):
        self.xPos = xPos  # int for row of bot
        self.yPos = yPos  # int for col of bot
        self.power = power  # int for how many spaces a bot can push another bot
        self.speed = speed  # int for how many spaces a bot can move
        self.color = color
        self.turn = turn
        self.failProb = .2
        self.botType = botType
        self.strategy = strategy

    def getLegalActions(self, state, world):
        actions = []
        sumoGrid = world.getSumoGrid()

        # For now just return 1 space to the 'West', 'East', 'North', 'South'
        if sumoGrid[state[0] + 1][state[1]] != -9:
            actions.append('East')

        if sumoGrid[state[0] - 1][state[1]] != -9:
            actions.append('West')

        if sumoGrid[state[0]][state[1] - 1] != -9:
            actions.append('North')

        if sumoGrid[state[0]][state[1] + 1] != -9:
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
            # divide the prob of failure equally among the wrong actions
            pWrongAction = self.failProb / (numActions - 1)
            for actionAttempt in legalActions:
                transModel[state, actionAttempt] = {}
                for actionOccur in legalActions:
                    nextState = self.nextState(state, actionOccur)
                    if actionAttempt == actionOccur:
                        # prob of performing the correct action
                        transModel[(state, actionAttempt)][nextState] = 1 - self.failProb
                    else:
                        transModel[(state, actionAttempt)][nextState] = pWrongAction
        return transModel

    def state(self):
        return (self.xPos, self.yPos)

    def nextState(self, state, action):
        xPos = state[0]
        yPos = state[1]
        if action == 'West':
            xPos = state[0] - 1
        elif action == 'East':
            xPos = state[0] + 1
        elif action == 'North':
            yPos = state[1] - 1
        elif action == 'South':
            yPos = state[1] + 1

        return (xPos, yPos)

    def isAt(self, xPos, yPos):
        return self.xPos == xPos and self.yPos == yPos

    def isTurn(self):
        return self.turn

    def toggleTurn(self):
        self.turn = not self.turn

    def randomizeAction(self, action,world):
	state = []
	state.append(self.xPos)
	state.append(self.yPos)

	legalActions = self.getLegalActions(state,world)
	weightedActions = []
	distributionSpread = self.failProb / (len(legalActions) - 1)

	for legalAction in legalActions:
	    if legalAction == action:
		weightedActions.append((legalAction,(1-self.failProb)))
	    else:
		weightedActions.append((legalAction,distributionSpread))

	space = {}
        current = 0
	
        for choice, weight in weightedActions:
            if weight > 0:
                space[current] = choice
                current += weight
        rand = random.uniform(0, current)
        for key in sorted(space.keys() + [current]):
            if rand < key:
                return choice
            choice = space[key]

	return action

