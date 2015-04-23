import argparse
from strategies.STRATEGIES import key_to_strategy
from strategies import STRATEGIES
from models.World import  World

__author__ = 'Nick'

def train_value_iteration():
    world = World({1: STRATEGIES.VALUE_ITERATION, 2: STRATEGIES.VALUE_ITERATION}, False)

    # Check for read/write errors.
    old = world.bot1.strategy.U
    world.bot1.strategy.U = None
    world.bot1.strategy.load_from_store()
    new = world.bot1.strategy.U

    for key in old:
        if old[key] != new[key]:
            print "Difference between read/write"
            return
    for key in new:
        if old[key] != new[key]:
            print "Difference between read/write"
            return
    print "Read/Write to store was performed correctly for value iteration."

def train_q_learning(cycles):
    world = World({1: STRATEGIES.Q_LEARNING, 2: STRATEGIES.VALUE_ITERATION}, False)
    world.epsilon = 0.5
    world.reset_game()
    print "Before: %s" % (world.bot1.strategy.Q.values)

    for i in xrange(cycles):
        if world.game_over:
            world.reset_game()
        world.update()
        world.update()

    print "After: %s" % (world.bot1.strategy.Q.values)
    old = world.bot1.strategy.Q.values
    world.bot1.strategy.save_to_store()

    # Check for read/write errors.
    world.bot1.strategy.Q.values = None
    world.bot1.strategy.load_from_store()
    new = world.bot1.strategy.Q.values

    for key in old:
        if old[key] != new[key]:
            print "Difference between read/write"
            return
    for key in new:
        if old[key] != new[key]:
            print "Difference between read/write"
            return
    print "Read/Write to store was performed correctly for q-learning."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SumoBot Arena")
    parser.add_argument("-c", "--cycles", type=int, default=10000, help="The number of training cycles to run.")
    parser.add_argument("trainee", help="The strategy to train.", choices=["v", "q"])
    args = parser.parse_args()
    args.trainee = key_to_strategy(args.trainee)

    if args.trainee == STRATEGIES.VALUE_ITERATION:
        train_value_iteration()
    elif args.trainee == STRATEGIES.Q_LEARNING:
        train_q_learning(args.cycles)

    print "Training complete!"
