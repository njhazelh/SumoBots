import shelve
from strategies.Strategy import Strategy
from strategies.valueIteration import runValueIteration

class ValueIterStrategy(Strategy):
    def __init__(self, me_bot, other_bot, world, from_store=True):
        self.me_bot = me_bot
        self.other_bot = other_bot
        self.world = world
        self.load_strategy(from_store)

    def load_strategy(self, from_store):
        if not from_store or not self.load_from_store():
            if self.me_bot == self.world.bot1:
                self.U = runValueIteration(self.world, self.me_bot, self.other_bot)
            elif self.me_bot == self.world.bot2:
                self.U = runValueIteration(self.world, self.other_bot, self.me_bot)
            self.save_to_store()

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


    def load_from_store(self):
        world_id = "%d:%d:%d" % (self.world.cols, self.world.rows, self.world.ring_radius)
        store = shelve.open("value_iteration_store")
        if store.has_key(world_id):
            self.U = store[world_id]
            store.close()
            return True
        else:
            store.close()
            return False

    def save_to_store(self):
        world_id = "%d:%d:%d" % (self.world.cols, self.world.rows, self.world.ring_radius)
        store = shelve.open("value_iteration_store")
        store[world_id] = self.U
        store.close()

    def __str__(self):
        return str(self.U)
