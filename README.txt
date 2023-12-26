# Pathfinder Visualizer

Pathfinder Visualizer is an interactive visualization tool for demonstrating pathfinding algorithms. It currently supports A* (A star) and Breadth First Search (BFS) algorithms, allowing users to visually understand how these algorithms traverse a grid to find the shortest path between two points.

## Features

- Interactive grid to set start and target nodes.
- Ability to place and remove barriers with mouse clicks.
- Real-time visualization of algorithm processing.
- Supports A* and BFS pathfinding algorithms.
- Adjustable volume for sound effects.
- User-friendly interface with instructions on how to use the visualizer.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the Pathfinder Visualizer, you need to have Pygame, Pygame_menu, and Numpy installed on your system. They can be installed like this:


pip install pygame pygame_menu numpy

Installing

To get the visualizer up and running, follow these steps:

    Clone the repository to your local machine:

bash

git clone https://github.com/your-username/pathfinder-visualizer.git

    Navigate to the cloned directory:

bash

cd pathfinder-visualizer

    Run the program:

bash

python pathfinder.py

Usage

When you run the Pathfinder Visualizer, you will be greeted with a start menu that provides the following instructions:

    Click to place the start node.
    Click to place the target node.
    Click/hold to place barriers.
    Press SPACE for A* algorithm, B for BFS.
    Press C to reset, X to keep barriers.
    Hold right click to remove nodes.

Adjust the volume as needed using the slider, and click 'Start' to begin visualizing the pathfinding algorithms.
Contributing

Created by Mohammad Baqer