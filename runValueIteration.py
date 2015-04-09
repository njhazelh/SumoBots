import util
from MDP import MDP
from valueIteration import valueIteration

# This function creates robot states, actions, a transition model, and
# a gamma. Then, using these models, it creates 2 robot classes. Then,
# It develops an MDP for the two robots. Finally, it runs a value iteration 
# algorithm on the MDP to develop a utility function for each MDP state

def runValueIteration():

	# robot states
	states = [(1,1), (1,2), (2,1), (2,2)]

	# robot actiosn from each state
	actions = {(1,1): ['up', 'right'],
			   (1,2): ['up', 'left'],
			   (2,1): ['down', 'right'],
			   (2,2): ['down', 'left']}

	# robot transition model
	transModel = {}
	transModel[((1,1), 'up')] = {(2,1): 0.8, (1,2): 0.2}
	transModel[((1,1), 'right')] = {(1,2): 0.8, (2,1): 0.2}
	transModel[((1,2), 'up')] = {(2,2): 0.8, (1,1): 0.2}
	transModel[((1,2), 'left')] = {(1,1): 0.8, (2,2): 0.2}
	transModel[((2,1), 'down')] = {(1,1): 0.8, (2,2): 0.2}
	transModel[((2,1), 'right')] = {(2,2): 0.8, (1,1): 0.2}
	transModel[((2,2), 'down')] = {(1,2): 0.8, (2,1): 0.2}
	transModel[((2,2), 'left')] = {(2,1): 0.8, (1,2): 0.2}

	# discount factor
	gamma = .3

	# 2 robot objects
	robot1 = Robot(states, actions, transModel)
	robot2 = Robot(states, actions, transModel)

	# MDP object
	mdp = MDP(robot1, robot2, gamma)

	# utility function for the MDP
	U = valueIteration(mdp, .001)

	# print out final utilities for the MDP
	for state in mdp.states:
		print 'U of ', state,' is ', U[state]
	
class Robot:

	def __init__(self, states, actions, transModel):
		self.states = states
		self.actions = actions
		self.transModel = transModel