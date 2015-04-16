import util
from MDP import MDP
from valueIteration import valueIteration
from World import World

# This function creates robot states, actions, a transition model, and
# a gamma. Then, using these models, it creates 2 robot classes. Then,
# It develops an MDP for the two robots. Finally, it runs a value iteration 
# algorithm on the MDP to develop a utility function for each MDP state

def runValueIteration(world, robot1, robot2, gamma, eps):

	# MDP object
	mdp = MDP(world, robot1, robot2, gamma)

	# utility function for the MDP
	U = valueIteration(mdp, eps)

	return U

	# print out final utilities for the MDP
	#for state in mdp.states:
	#	print 'U of ', state,' is ', U[state]
