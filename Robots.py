
from HumanStrategy import HumanStrategy
from Robot import Robot


def HumanRobot():
    human_control = HumanStrategy()
    robot = Robot(human_control)
    return robot
