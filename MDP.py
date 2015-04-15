import util
class MDP:
    """
    This class represents the Markov Decision Process in the sumoBots world.
    It consists of a set of states, actions, a transition model, rewards, and
    a discount factor
    """

    def __init__(self, world, robot1, robot2, gamma):
        self.world = world
        self.robot1 = robot1
        self.robot2 = robot2
        self.states = self.get_states()
        self.actions = self.get_actions()
        self.transModel = self.get_transModel()
        self.rewards = self.get_rewardModel()
        self.gamma = gamma

    def get_states(self):
        """
        The MDP state space is all possible board configurations. This is all possible
        arrangements of both robots, as well as whose turn it is. The number at the
        beginning of the tuple in the MDP state is which robot's turn it is
        """

        robot1states = self.world.getStates()
        robot2states = self.world.getStates()

        mdpStates = []

        for turn in [1, 2]:
            for state1 in robot1states:
                for state2 in robot2states:
                    mdpStates.append((turn, state1, state2))

        return mdpStates

    def get_actions(self):
        """
        The MDP actions are stored in a dictionary. The key is the state and the value is a
        list of possible actions which can be taken from that state.
        """

        robot1actions = self.robot1.getAllActions(self.world)
        robot2actions = self.robot2.getAllActions(self.world)

        mdpActions = {}

        for mdpState in self.states:
            if self.is_rob1(mdpState):
                mdpActions[mdpState] = robot1actions[mdpState[1]]
            else:
                mdpActions[mdpState] = robot2actions[mdpState[2]]

        return mdpActions

    def get_transModel(self):
        """
        The MDP transition model is a dictionary where a key is a (state, action) tuple, and
        the value is another dictionary. In this dictionary, a key is a possible nextState,
        and the value is the probability of a robot transitioning from state to nextState.
        """
        robot1actions = self.robot1.getAllActions(self.world)
        robot2actions = self.robot2.getAllActions(self.world)

        robot1_transModel = self.robot1.getTransitionModel(self.world)
        robot2_transModel = self.robot2.getTransitionModel(self.world)

        mdp_transModel = {}

        for mdpState in self.states:
            if self.is_rob1(mdpState):
                actions = robot1actions[mdpState[1]]    # possible actions robot 1 can take from its current state
                for action in actions:
                    newStateDist = robot1_transModel[(mdpState[1], action)]
                    currTransModel = {}
                    for (newState, prob) in newStateDist.items():
                        currTransModel[(2, newState, mdpState[2])] = prob
                    mdp_transModel[(mdpState, action)] = currTransModel
            else:
                actions = robot2actions[mdpState[2]]
                for action in actions:
                    newStateDist = robot2_transModel[(mdpState[2], action)]
                    currTransModel = {}
                    for newState, prob in newStateDist.items():
                        currTransModel[(1, mdpState[1], newState)] = prob
                    mdp_transModel[(mdpState, action)] = currTransModel

        return mdp_transModel

    def get_rewardModel(self):
        """
        We are using a simplified reward system to start with
        """

        mdpRewards = {}
        for mdpState in self.states:
            dist = straightLineDist(mdpState[1], mdpState[2])
            if dist == 0:
                mdpRewards[mdpState] = 15
            else:
                mdpRewards[mdpState] = 15 - straightLineDist(mdpState[1], mdpState[2])
        return mdpRewards

    # returns true if it is robot 1's turn
    def is_rob1(self, mdpState):
        return mdpState[0] == 1

def straightLineDist(state1,state2):
    x1 = state1[0]
    y1 = state1[1]

    x2 = state2[0]
    y2 = state2[1]

    dist = pow((pow(abs(x1 - x2),2) + pow(abs(y1 - y2),2)), 0.5)

    return dist
