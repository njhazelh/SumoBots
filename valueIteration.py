import util

def valueIteration(MDP, eps):
	"""
	The value iteration algorithm calculates the utility of each state in the MDP. This
	utility is then used to determine which action a robot should take, given it's current
	state and possible actions from that state. Once the change in utility is less than
	eps, the while loop terminates
	"""

	# this will hold all utility information
	U = util.Counter()

	# when this term become true, the while loop terminates
	keep_iterating = True
	while keep_iterating: 

		# loop through each state on each iteration
		for mdpState in MDP.states:

			# will store the maximum utility out of all possible actions
			maxVal = 0
			for action in MDP.actions[mdpState]:

				# will sum the utilities over all possible states from that action
				sum = 0
				for (nextState, prob) in MDP.transModel[(mdpState, action)].items():
					#print 'this is the next state', nextState
					#print 'this is the current state', mdpState
					nextReward = MDP.rewards[mdpState]
					oldUtil = U[nextState]
					sum += prob*(nextReward + MDP.gamma*oldUtil)
				maxVal = max(maxVal, sum)
			Uprev = U[mdpState]
		
			# update the utility for this state
			U[mdpState] = maxVal

			# if the utility value changes by less than eps, then stop iterating
			if abs(Uprev - U[mdpState]) < eps:
				keep_iterating = False
	return U