#!/usr/bin/python

import argparse
from Tkinter import Tk
from STRATEGIES import key_to_strategy
from scenes.SumoApp import SumoApp


__author__ = 'Nick'


def runGUI(args):
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    root.resizable(width=0, height=0)
    app = SumoApp(root, args.robot1, args.robot2)
    app.mainloop()

def runTraining(args):
    print args

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SumoBot Arena")
    parser.add_argument("-t", "--train", action="store_true", help="Runs training sessions without GUI")
    parser.add_argument("-c", "--cycles", type=int, default=1000, help="The number of training cycles to run.")
    parser.add_argument("-r1", "--robot1", help="robot 1's strategy", choices=["h", "v", "q"], default=None)
    parser.add_argument("-r2", "--robot2", help="robot 2's strategy", choices=["h", "v", "q"], default=None)
    args = parser.parse_args()

    args.robot1 = key_to_strategy(args.robot1)
    args.robot2 = key_to_strategy(args.robot2)

    if args.train:
        runTraining(args)
    else:
        runGUI(args)
