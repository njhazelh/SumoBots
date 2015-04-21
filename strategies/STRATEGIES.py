from strategies.HumanStrategy import HumanStrategy
from strategies.QLearnStrategy import QLearnStrategy
from strategies.ValueIterStrategy import ValueIterStrategy

__author__ = 'Nick'

HUMAN = 0
Q_LEARNING = 1
VALUE_ITERATION = 2

def enum_to_strategy(robot, other_bot, world, type):
    """
    Convert one of the values above into a strategy object.
    :param robot: The robot that this strategy applies to.
    :param world: The world that the strategy applies to.
    :param type: The type enum of the strategy.
    :return: A Strategy Object.
    """
    if type == HUMAN:
        return HumanStrategy(world)
    elif type == Q_LEARNING:
        return QLearnStrategy(robot, other_bot, world)
    elif type == VALUE_ITERATION:
        return ValueIterStrategy(robot, other_bot, world)
    else:
        raise Exception("Strategy not recognized: %s" % (type))

