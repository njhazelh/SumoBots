#!/usr/bin/python

import argparse
from Tkinter import Tk
from scenes.SumoApp import SumoApp


__author__ = 'Nick'


def main():
    root = Tk()
    root.title("Robot-Sumo [by Team Wall-E]")
    root.resizable(width=0, height=0)
    app = SumoApp(master=root)
    app.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SumoBot Arena")
    # parser.add_argument()
    main()
