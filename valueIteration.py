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
					total += prob*(MDP.rewards[nextState] + MDP.gamma*U[nextState])
				maxVal = max(maxVal, total)
			Uprev = U[mdpState]
		
			# update the utility for this state
			U[mdpState] = maxVal

			# if the utility value changes by less than eps, then stop iterating
			deltU = abs(Uprev - U[mdpState])
			maxDeltU = max(maxDeltU, deltU)
		if maxDeltU < eps:
			keep_iterating = False
	return U