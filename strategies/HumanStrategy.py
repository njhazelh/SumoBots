from strategies.Strategy import Strategy
import ACTIONS

__author__ = 'Nick'

# Keys
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"


def key_to_action(event):
    """
    Find which action maps to the key event.
    :param event: The key event the convert
    :return: The action that mapped to event
    """
    if event.keysym == UP:
        return ACTIONS.MOVE_NORTH
    elif event.keysym == DOWN:
        return ACTIONS.MOVE_SOUTH
    elif event.keysym == LEFT:
        return ACTIONS.MOVE_WEST
    elif event.keysym == RIGHT:
        return ACTIONS.MOVE_EAST
    else:
        raise Exception("Event does not map to action: %s" % (event.keysym))


class HumanStrategy(Strategy):
    """
    HumanStrategy is the strategy where a human controls the robot via key
    input.

    There are some interesting factors that come into play with this strategy.
    Mainly, tkinter runs a main loop that receives and dispatches events from the
    OS.  Unless we return to this loop once in a while, we will not receive any
    events and the application will freeze.  As such, choose_action can only check
    that there has been a key event.  If we were to busy-wait until
    there's a key, we would wait forever, and rest of the application would freeze.
    If there isn't a key-event that maps to an action, then we return None.
    This gets used by the rest of the application to avoid advancing the player turn.
    """

    def __init__(self, world):
        """
        Initialize the strategy
        :param world: The world that the strategy is operating in
        """
        Strategy.__init__(self)
        self.world = world

    def choose_action(self):
        """
        Check that there's a key-event that maps to an action.
        :return: If there's an event that maps to an action, return the action.
                 Else, return None.
        """
        if self.world.key_event is not None and \
                        self.world.key_event.keysym in [UP, DOWN, LEFT, RIGHT]:
            return key_to_action(self.world.key_event)
        else:
            return None
