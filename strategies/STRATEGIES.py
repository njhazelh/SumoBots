from strategies.HumanStrategy import HumanStrategy
from strategies.QLearnStrategy import QLearnStrategy
from strategies.ValueIterStrategy import ValueIterStrategy

__author__ = 'Nick'

HUMAN = 0
Q_LEARNING = 1
VALUE_ITERATION = 2

def enum_to_strategy(world, type):
    if type == HUMAN:
        return HumanStrategy()
    elif type == Q_LEARNING:
        return QLearnStrategy()
    elif type == VALUE_ITERATION:
        return ValueIterStrategy()
    else:
        raise Exception("Strategy not recognized: %s" % (type))

