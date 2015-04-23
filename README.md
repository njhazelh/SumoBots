#SumoBots
An final project for CS:4100/5100 Artificial Intelligence  and Capstone project.

This project aims to create a world in which sumo bots can battle each other using various AI algorithms to intelligently choose actions.

## Running the Program
- To be able to train the robot run
    > python sumo_trainer.py -c <gamesToTrain> q

- To be able to run the sumoBots program
    > python sumobots.py

##Rewards
- Negative reward for each turn.
- Huge reward for pushing opponent out of ring.
- Timeout at draw
  points based on:
  - dominance in battle
  - dominant position

## Robot Dynamics
Cool-down times but bigger/smaller moves.
Mana:
- actions use mana
- time recovers mana
- successful actions restore mana

###Variations
- Speed/power
- Non-deterministic actions
- Algorithm

## Components
Models: World / Robot
Controllers: Stategies for Algorithms
Views: Arena

## MVC
### Models
Robot
World

### View
Arena

### Controller
Strategy
