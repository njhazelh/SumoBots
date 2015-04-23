#SumoBots
An final project for CS:4100/5100 Artificial Intelligence  and Capstone project.

This project aims to create a world in which sumo bots can battle each other using various AI algorithms to intelligently choose actions.

## Running the Program
Both sumo_trainer.py and sumobots.py are executable Python 2.7 files, which can be run using ```./<file> ...```
or ```python <file> ...``` notation.

- To be able to train the robot run
    ```bash
    python sumo_trainer.py -c <gamesToTrain> q # Run gamesToTrain games to train Q-Learning
    # OR
    python sumo_trainer.py v   # Train the ValueIterator
    ```

- To be able to run the sumoBots program
    ```bash
    python sumobots.py # Run the default GUI
    # OR
    python sumobots.py [-h] [-r1 {q,v,h,r}] [-r2 {q,v,h,r}] # Run the GUI, but skip the configuration.
    ```
    
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
