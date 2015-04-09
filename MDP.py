class MDP:
	"""
	This class represents the Markov Decision Process in the sumoBots world.
	It consists of a set of states, actions, a transition model, rewards, and
	a discount factor
	"""
	def __init__(self, robot1, robot2, gamma):

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

		robot1states = self.robot1.states
		robot2states = self.robot2.states

		mdpStates = []

		for turn in [1,2]:
			for state1 in robot1states:
				for state2 in robot2states:
					mdpStates.append((turn, state1, state2))

		return mdpStates

	def get_actions(self):
		"""
		The MDP actions are stored in a dictionary. The key is the state and the value is a 
		list of possible actions which can be taken from that state.
		"""

		robot1actions = self.robot1.actions
		robot2actions = self.robot2.actions

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
		the value is another dictionaty. In this dictionary, a key is a possible nextState,
		and the value is the probability of a robot transitioning from state to nextState.
		"""

		robot1actions = self.robot1.actions
		robot2actions = self.robot2.actions

		robot1_transModel = self.robot1.transModel
		robot2_transModel = self.robot2.transModel

		mdp_transModel = {}

		for mdpState in self.states:
			if self.is_rob1(mdpState):
				actions = robot1actions[mdpState[1]]
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
					for newState in newStateDist.keys():
						currTransModel[(1, mdpState[1], newState)] = prob
					mdp_transModel[(mdpState, action)] = currTransModel

		return mdp_transModel

	def get_rewardModel(self):
		""" 
		We are using a simplified reward system to start with
		"""

		mdpRewards = {}
		for mdpState in self.states:
			if mdpState[1] == (2,1) and mdpState[2] == (1,2):
				mdpRewards[mdpState] = 10
			else:
				mdpRewards[mdpState] = 1

		return mdpRewards

	def is_rob1(self, mdpState):
		return mdpState[0] == 1