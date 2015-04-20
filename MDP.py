import util
class MDP:
    """
    This class represents the Markov Decision Process in the sumoBots world.
    It consists of a set of states, actions, a transition model, rewards, and
    a discount factor
    """

    def __init__(self, world, robot1, robot2):
        self.world = world
        self.robot1 = robot1
        self.robot2 = robot2
        self.states = self.getStates()
        self.actions = self.getActions()
        self.transModel = self.getTransModel()
        self.rewards = self.getNewRewardModel(world)

    def getStates(self):
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

    def getActions(self):
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

    def getTransModel(self):
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

    def getRewardModel(self):
        """
        We are using a simplified reward system to start with
        """

        mdpRewards = {}
        for mdpState in self.states:
            dist = util.manhattanDistance(mdpState[1], mdpState[2])
            if dist == 0:
                mdpRewards[mdpState] = 15
            else:
                mdpRewards[mdpState] = 15 - dist
        return mdpRewards
    
    def getNewRewardModel(self, world):
        """
        Using this function, rewards are based on robot's position according to how close it is to 
        the boundary, as well as if the robot is between the other robot, and the closest boundary.
        """
        mdpRewards = {}
        rows = world.getNumRows()
        cols = world.getNumCols()
        cx = (cols - 1) / 2.0
        cy = (rows - 1) / 2.0
        for mdpState in self.states:
            dist = util.manhattanDistance(mdpState[1], mdpState[2])
            mdpRewards[mdpState] = 15 - dist

            rob1Pos = mdpState[1]
            rob1RowPos = rob1Pos[0]
            rob1ColPos = rob1Pos[1]
            rob1DCenter = ((rob1ColPos - cx) ** 2 + (rob1RowPos - cy) ** 2) ** 0.5
            
            rob2Pos = mdpState[2]
            rob2RowPos = rob2Pos[0]
            rob2ColPos = rob2Pos[1]
            rob2DCenter = ((rob2ColPos - cx) ** 2 + (rob2RowPos - cy) ** 2) ** 0.5
            
            if self.is_rob1(mdpState):
                #Check to see whether the robot is on the edge of the boundary
                if round(rob1DCenter) == world.ring_radius and round(rob2DCenter) <= world.ring_radius:
                    mdpRewards[mdpState] -= 10
                    #If robot is on boundary and next to the opponent
                    if dist == 1:
                        mdpRewards[mdpState] -= 10
            else:
                if round(rob2DCenter) == world.ring_radius and round(rob1DCenter) <= world.ring_radius:
                    mdpRewards[mdpState] -= 10
                    if dist == 1:
                        mdpRewards[mdpState] -= 10
    
        return mdpRewards
            
    

    # returns true if it is robot 1's turn
    def is_rob1(self, mdpState):
        return mdpState[0] == 1