#!/usr/bin/python

import argparse
from Tkinter import Tk

from strategies.STRATEGIES import key_to_strategy
from scenes.SumoApp import SumoApp


__author__ = 'Nick'


def runGUI(args):
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    root.resizable(width=0, height=0)
    app = SumoApp(root, args.robot1, args.robot2)
    app.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SumoBot Arena")
    parser.add_argument("-r1", "--robot1", help="robot 1's strategy", choices=["h", "v", "q"], default=None)
    parser.add_argument("-r2", "--robot2", help="robot 2's strategy", choices=["h", "v", "q"], default=None)
    args = parser.parse_args()
    args.robot1 = key_to_strategy(args.robot1)
    args.robot2 = key_to_strategy(args.robot2)
    runGUI(args)
