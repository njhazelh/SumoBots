import util
from MDP import MDP

def valueIteration(MDP, gamma, delta):
    """
    The value iteration algorithm calculates the utility of each state in the MDP. This
    utility is then used to determine which action a robot should take, given it's current
    state and possible actions from that state. Once the change in utility is less than
    delta, the while loop terminates
    """

    # this will hold all utility information
    U = util.Counter()
    allActions = MDP.getActions()
    # when this term become true, the while loop terminates
    keep_iterating = True
    while keep_iterating:
        maxDeltU = 0
        # loop through each state on each iteration
        for mdpState in MDP.states:
            # will store the maximum utility out of all possible actions
            maxVal = 0

            for action in allActions[mdpState]:
                # will sum the utilities over all possible states from that action
                total = 0
                for (nextState, prob) in MDP.transModel[(mdpState, action)].items():
                    total += prob * (MDP.rewards[nextState] + gamma * U[nextState])
                maxVal = max(maxVal, total)
            Uprev = U[mdpState]

            # update the utility for this state
            U[mdpState] = maxVal

            # if the utility value changes by less than delta, then stop iterating
            deltU = abs(Uprev - U[mdpState])
            maxDeltU = max(maxDeltU, deltU)
        if maxDeltU < delta:
            keep_iterating = False
    return U


def runValueIteration(world, robot1, robot2):
    """
    This function creates robot states, actions, a transition model, and
    a gamma. Then, using these models, it creates 2 robot classes. Then,
    It develops an MDP for the two robots. Finally, it runs a value iteration
    algorithm on the MDP to develop a utility function for each MDP state
    :param world:
    :param robot1:
    :param robot2:
    :param gamma:
    :param delta:
    :return:
    """
    # MDP object
    mdp = MDP(world, robot1, robot2)

    # utility function for the MDP
    U = valueIteration(mdp, world.gamma, world.delta)

    return U

    # print out final utilities for the MDP
    # for state in mdp.states:
    # print 'U of ', state,' is ', U[state]
