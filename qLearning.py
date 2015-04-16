import util

class QLearning:
    """
    Q(s,a) <- (1 - alpha)Q(s,a) + (alpha)[reward + gamma*maxQ(s',a')]
    We want alpha to decay over time, because the estimates will continue
    to get better, so we will want to follow those estimates more later on
    in the algorithm.

    Exploration function will take a value estimate u and a visit count n.
    f(u,n) = u + k/n. k is a constant.

    Q update with optimistic exploration function will be:
        Q(s,a) = (1-alpha)Q(s,a) + (alpha)R(s,a,s') + gamma*max(f(Q(s',a'), N(s',a')))
            N(s',a') is the count n of the number of times this state is visited
    """

    def __init__(self):
        self.values = util.Counter()

    def getQValue(self, state, action):
        """
        Returns the current q-value of the state action pair.
        Returns 0.0 if state has not been visited.
        """
        return self.values[(state, action)]

    def computeValueFromQValues(self, state, world, robot):
        """
        returns max_action Q(state, action) over legal actions.
        No legal actions returns 0.0
        """

        actions = robot.getLegalActions(state, world)

        if world.isGameOver():
            return 0.0

        bestValue = self.getQValue(state, actions[0])

        for action in actions:
            if self.getQValue(state, action) > bestValue:
                bestValue = self.getQValue(state, action)

        return bestValue

    def computeActionFromQValues(self, state, world, robot):
        """
        Compute the best action to take given the state
        """

        actions = robot.getLegalActions(state, world)

        if world.isGameOver():
            return None

        bestAction = actions[0]
        bestValue = self.getQValue(state, bestAction)

        for action in actions:
            if self.getQValue(state, action) > bestValue:
                bestAction = action
                bestValue = self.getQValue(state, action)
            elif self.getQValue(state, action) == bestValue:
                bestAction = random.choice([action, bestAction])

        return bestAction

    def getAction(self, state, epsilon, world, robot):
        """
        Compute action to take from state. epsilon is the probability of taking a random action.
        """

        legalActions = robot.getLegalActions(state)
        action = None

        randomChoice = util.flipCoin(epsilon)

        if world.isGameOver():
            return None

        if randomChoice:
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state, world, robot)

        return action

    def update(self, state, action, nextState, reward, world, robot, alpha, gamma):
        """
        Update the Q-Value
        """

        prevQVal = self.getQValue(state, action)
        nextQVal = self.computeActionFromQValues(nextState)
        newValue = (1-alpha) * prevQVal + alpha*(reward + gamma*nextQVal)

        self.values[(state, action)] = newValue



