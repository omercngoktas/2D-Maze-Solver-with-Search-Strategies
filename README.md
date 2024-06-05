# 2D Maze Solver with Search Strategies

## Overview
This project implements a solver for 2D mazes using various search strategies. The solver supports the following strategies:
- Depth First Search
- Breadth First Search
- Iterative Deepening
- Uniform Cost Search
- Greedy Best First Search
- A* Heuristic Search

The solver takes a maze file as input, where each square in the maze can contain either an "S" (starting point), "G" (goal square), or "T" (trap square). The cost of each move is one point, but moving onto a trap square increases the cost by 6. The solver finds the goal state, the cost of the solution, the solution path, and the list of expanded nodes for each search strategy.

## Features
- Implementation of 2D maze solver with various search strategies
- Support for solving mazes with starting, goal, and trap squares
- Evaluation of goal state, solution cost, solution path, and expanded nodes for each search strategy
- Text-based interface for input and output
- Design document describing classes, fields, methods, and search strategies used in the project
- Output files containing results for each search strategy
- Support for running simulations and reporting mean and standard deviation of rewarded points

## Project Structure
- `src/`: Contains the source code for the maze solver and search strategies implementation
- `docs/`: Includes the design document

## Usage
Execute main.py file under src folder.

