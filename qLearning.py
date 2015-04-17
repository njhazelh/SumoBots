import util
import random
from MDP import MDP

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

    *** states for Q learning are the same as MDP state, eg. (1, (15,15), (18,19)) or 
    (the number of the robot whose turn it is, rob1 state, rob2 state)
    """

    def __init__(self, world, robot1, robot2):
        self.values = util.Counter()
        self.mdp = MDP(world, robot1, robot2)

    def getQValue(self, state):
        """
        Returns the current q-value of the state.
        Returns 0.0 if state has not been visited.
        """
        return self.values[state]

    def computeActionFromQValues(self, world, robot):
        """
        Compute the best action to take given the state based on Q values
        """

        if robot == world.bot1:
            turn = 1
            nextTurn = 2
            qState = (1, world.bot1.state(), world.bot2.state())
            nextOppBotState = world.bot2.state()
        elif robot == world.bot2:
            turn = 2
            nextTurn = 1
            qState = (2, world.bot1.state(), world.bot2.state())
            nextOppBotState = world.bot1.state()

        actions = robot.getLegalActions(robot.state(), world)

        if world.isGameOver():
            return None

        bestValue = self.getQValue(qState)
        bestAction = actions[0]

        for action in actions:

            nextBotstate = robot.nextState(robot.state(), action)
            if turn == 1:
                nextQstate = (2, nextBotstate, nextOppBotState)
            elif turn == 2:
                nextQstate = (1, nextOppBotState, nextBotstate)

            if self.getQValue(nextQstate) > bestValue:
                bestValue = self.getQValue(nextQstate)
                bestAction = action
            elif self.getQValue(nextQstate) == bestValue:
                bestAction = random.choice([action, bestAction])

        return bestValue

    def computeValueFromQValues(self, qState, world, robot):
        """
        Compute the value of taking best action, given the state
        """

        if robot == world.bot1:
            turn = 1
            nextTurn = 2
            nextOppBotState = world.bot2.state()
        elif robot == world.bot2:
            turn = 2
            nextTurn = 1
            nextOppBotState = world.bot1.state()

        actions = robot.getLegalActions(robot.state(), world)

        if world.isGameOver():
            return 0.0

        bestValue = self.getQValue(qState)

        for action in actions:

            nextBotstate = robot.nextState(robot.state(), action)
            if turn == 1:
                nextQstate = (2, nextBotstate, nextOppBotState)
            elif turn == 2:
                nextQstate = (1, nextOppBotState, nextBotstate)

            if self.getQValue(nextQstate) > bestValue:
                bestValue = self.getQValue(nextQstate)

        return bestValue

    def getAction(self, world, robot):
        """
        Compute action to take from state. epsilon is the probability of taking a random action.
        """
        epsilon = world.epsilon
        state = robot.state()
        legalActions = robot.getLegalActions(state, world)
        action = None

        randomChoice = util.flipCoin(epsilon)

        if world.isGameOver():
            return None

        if randomChoice:
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(world, robot)

        return action

    def update(self, world, robot):
        """
        Update the Q-Value
        """
        alpha = world.alpha
        gamma = world.gamma
        bot1state = world.bot1.state()
        bot2state = world.bot2.state()

        if robot == world.bot1:
            qState = (1, bot1state, bot2state)
        elif robot == world.bot2:
            qState = (2, bot1state, bot2state)

        reward = self.mdp.rewards[qState]

        oldQVal = self.getQValue(qState)
        maxVal = self.computeValueFromQValues(qState, world, robot)
        newValue = (1-alpha) * oldQVal + alpha*(reward + gamma*oldQVal)

        self.values[qState] = newValue