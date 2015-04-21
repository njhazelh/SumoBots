__author__ = 'Nick'

class Strategy(object):
    """
    Strategy encapsulates the decision making process that a robot makes
    using available world state and input.
    """
    def choose_action(self):
        """
        Choose an action according to this strategy.
        :return: The action chosen.
        """
        raise NotImplementedError()

    def update(self):
        """
        Update the strategy after a move.  Intended for learning algorithms.
        """
        pass
