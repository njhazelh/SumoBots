from strategies.Strategy import Strategy
from valueIteration import runValueIteration

__author__ = 'Nick'


class ValueIterStrategy(Strategy):
    def __init__(self, me_bot, other_bot, world):
        self.me_bot = me_bot
        self.other_bot = other_bot
        self.world = world
        self.load_strategy()

    def load_strategy(self):
        self.U = runValueIteration(self.world, self.me_bot, self.other_bot)

    def choose_action(self):
        enemy_state = self.other_bot.state

        max_util = None
        best_action = None

        # Perform Argmax over available actions.
        for action in self.me_bot.get_legal_actions():
            next_state = self.me_bot.next_state(action)
            if self.me_bot.id == 1:
                next_util = self.U[(2, next_state, enemy_state)]
                if max_util is None or next_util > max_util:
                    max_util = next_util
                    best_action = action
            elif self.me_bot.id == 2:
                next_util = self.U[(1, next_state, enemy_state)]
                if max_util is None or next_util > max_util:
                    max_util = next_util
                    best_action = action

        return best_action
