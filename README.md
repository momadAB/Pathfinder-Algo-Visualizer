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

You will need Python (version 3.6 or higher) and the following Python packages: `pygame`, `pygame_menu`, and `numpy`. You can install them using the following command:

```bash
pip install pygame pygame_menu numpy
```

To get the visualizer up and running, follow these steps:

Clone the repository to your local machine:

    git clone https://github.com/your-username/pathfinder-visualizer.git

Navigate to the cloned directory:

    cd /PATH/TO/pathfinder-visualizer

Run the program:

    python pathfinder.py

Usage

Upon launching the Pathfinder Visualizer, a start menu will display the following instructions:

    Click for the first time to place the start node.
    Click a second time to place the target node.
    Click/hold to draw barriers.
    Press SPACE to execute the A* algorithm, or B for BFS.
    Press C to clear the grid, or X to retain barriers.
    Right-click to remove nodes.

Adjust the volume with the slider and click 'Start' to begin the visualization.

Created by Mohammad Baqer
