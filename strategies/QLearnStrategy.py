import shelve
from strategies.Strategy import Strategy
from qLearning import QLearning

class QLearnStrategy(Strategy):
    def __init__(self, robot, otherbot, world, from_store=True):
        self.robot = robot
        self.otherbot = otherbot
        self.world = world
        self.Q = QLearning(world, robot, otherbot)
        self.load_strategy(from_store)

    def load_strategy(self, from_store):
        if from_store: self.load_from_store()

    def choose_action(self):
        return self.Q.getAction(self.world, self.robot)

    def update(self):
        self.Q.update(self.world, self.robot)

    def __str__(self):
        return str(self.Q)

    def load_from_store(self):
        world_id = "%d:%d:%d" % (self.world.cols, self.world.rows, self.world.ring_radius)
        store = shelve.open("q_learn_store")
        if store.has_key(world_id):
 	    print "Q-Learning Store Loaded!"
            self.Q.values = store[world_id]
        store.close()

    def save_to_store(self):
        world_id = "%d:%d:%d" % (self.world.cols, self.world.rows, self.world.ring_radius)
        store = shelve.open("q_learn_store")
        store[world_id] = self.Q.values
        store.close()
