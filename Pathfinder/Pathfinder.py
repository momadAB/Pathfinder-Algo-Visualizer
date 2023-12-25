# Pathfinder algorithm visualizer with A star algorithm and Breadth First Search algorithm
import time
import threading
import pygame
import pygame_menu
import random
from pathlib import Path
import ctypes
from sound_player import play_sound_for_rect, create_sweep_sound
from visual_node import VisualNode

# Load kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Define Sleep function
usleep = kernel32.Sleep

sound = Path(__file__).with_name('button-6.wav')

sound2 = r"button-6.wav"
# Diagonal cost: approximation of 10*sqrt(2), which would be the length of the hypotenuse of a right triangle of sides
# length 10
DIAGONAL_COST = 14
STRAIGHT_COST = 10
# Keep the ratio between the grids and window dimensions the same or there will be animation problems
GRID_X = 60
GRID_Y = 40

windowHeight = 800
windowWidth = 1200
# Color constants
BLACK = (100, 100, 100)
WHITE = (54, 54, 54)
PURPLE = (209, 60, 232)
ORANGE = (230, 163, 69)
LAVENDER = (230, 230, 250)
SLATE_GREY = (112, 128, 144)
TEAL = (50, 222, 170)


# Calculates the overall cost
def get_distance(node1, node2):
    y_diff = abs(node1.x - node2.x)
    x_diff = abs(node1.y - node2.y)

    if x_diff > y_diff:
        diagonal_movements = y_diff
        x_diff = x_diff - y_diff
        return (DIAGONAL_COST * diagonal_movements) + (STRAIGHT_COST * x_diff)

    diagonal_movements = x_diff
    y_diff = y_diff - x_diff
    return (DIAGONAL_COST * diagonal_movements) + (STRAIGHT_COST * y_diff)


# Reset every node except start, target, and barriers
def reset_from_search(grid, win):
    for row in grid:
        for node in row:
            if node.color == SLATE_GREY or node.color == LAVENDER or node.color == TEAL:
                # node.set_color(WHITE)
                node.set_color(WHITE)
                update_node(node, win)


def retrace_path(self, window, duration=1.0):
    path_back = []
    if self.parent:
        current_node = self
        while current_node.parent:  # Traces back path from nodes parents, not including start and end nodes
            path_back.append(current_node)
            current_node = current_node.parent

        print(path_back)
        # Randomly shuffle the path nodes, excluding the starting node (which is the last one in path_back)
        random.shuffle(path_back)
        node_count = len(path_back)
        delay_per_node = duration / node_count if node_count else 0
        print(path_back)

        # Draw the nodes in the random order
        for node in path_back:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
            if node.color is not ORANGE and node.color is not PURPLE:
                node.set_color(TEAL)
                pygame.time.wait(int(delay_per_node * 1000))
                play_sound_for_rect(node, GRID_X, GRID_Y)
                node.draw(window)
            pygame.display.update()  # Update the display to reflect the changes

    return path_back


# A* pathfinding algorithm
def a_star_algo(startNode, targetNode, grid, window):
    reset_from_search(grid, window)
    openSet = []
    closedSet = []
    startNode.gCost = 0
    targetNode.gCost = 0
    startNode.hCost = get_distance(startNode, targetNode)
    targetNode.hCost = 0

    openSet.append(startNode)
    i = 1
    while openSet:
        currentNode = openSet[0]

        for node in openSet:
            if node == openSet[0]:
                continue
            if node.get_f_cost() < currentNode.get_f_cost() or (
                    node.get_f_cost() == currentNode.get_f_cost() and node.hCost < currentNode.hCost):
                currentNode = node

        openSet.remove(currentNode)
        closedSet.append(currentNode)

        if currentNode is not startNode:
            currentNode.set_color(SLATE_GREY)
            update_node_with_animation(currentNode, window)

        for neighbor in currentNode.get_neighbors(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")

                return retrace_path(neighbor, window)

            if neighbor.check_state() != "walkable" or neighbor in closedSet:
                continue

            costToNeighbor = currentNode.gCost + get_distance(currentNode, neighbor)
            if costToNeighbor < neighbor.gCost or neighbor not in openSet:
                neighbor.gCost = costToNeighbor
                neighbor.hCost = get_distance(neighbor, targetNode)
                neighbor.parent = currentNode

                if neighbor not in openSet:
                    openSet.append(neighbor)
                    if neighbor is not startNode and neighbor.color is not SLATE_GREY:
                        # pygame.mixer.music.play()
                        play_sound_for_rect(neighbor, GRID_X, GRID_Y)
                        neighbor.set_color(LAVENDER)
                        update_node(neighbor, window)

    print("Path not found")
    return []


# Breadth First Search pathfinding algorithm
def bfs_algo(startNode, targetNode, grid, window):
    reset_from_search(grid, window)
    visited = []
    queue = []
    visited.append(startNode)
    queue.append(startNode)

    while queue:
        currentNode = queue.pop(0)

        if currentNode is not startNode:
            # pygame.mixer.music.play()
            currentNode.set_color(SLATE_GREY)
            usleep(1)
            play_sound_for_rect(neighbor, GRID_X, GRID_Y)
            update_node(currentNode, window)

        for neighbor in currentNode.get_neighbors_straight(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")
                return retrace_path(neighbor, window)

            if neighbor.check_state() != "walkable":
                continue

            if neighbor is not startNode and neighbor.color is not SLATE_GREY:
                # pygame.mixer.music.play()
                neighbor.set_color(LAVENDER)
                update_node(neighbor, window)

            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                neighbor.parent = currentNode


# Update visuals of node
def update_node(node, window):
    node.draw(window)
    pygame.display.update(node.rect)


# Update visuals of node with an animation and threading
def update_node_with_animation(node, window):
    d = threading.Thread(target=node.draw_with_longer_animation(window))
    d.start()
    pygame.display.update(node.rect)


# Convert x, y coordinates into grid values
def coord_to_grid(coord):
    x, y = coord

    column = x // (windowWidth // GRID_X)
    row = y // (windowHeight // GRID_Y)

    return column, row


def draw_grid(win):
    grid = []
    # Populate grid
    for i in range(GRID_Y):
        grid.append([])
        for j in range(GRID_X):
            node = VisualNode(i, j)
            grid[i].append(node)

    # Make outline
    for node in grid[0]:
        node.set_color(BLACK)
    for node in grid[GRID_Y - 1]:
        node.set_color(BLACK)
    vertical1 = []
    vertical2 = []
    for list in grid:
        vertical1.append(list[0])
        vertical2.append(list[GRID_X - 1])
    for node in vertical1:
        node.set_color(BLACK)
    for node in vertical2:
        node.set_color(BLACK)

    # Draw nodes in grid
    for row in grid:
        for node in row:
            node.draw(win)

    pygame.display.update()

    return grid


# Start menu of the program which tells the user how to use the program
def menu():
    pygame.init()

    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")
    menu = pygame_menu.Menu('Welcome', windowWidth, windowHeight,
                            theme=pygame_menu.themes.THEME_BLUE)

    def start():
        menu.close()
        main()

    menu.add.label("Steps to using Pathfinder Visualizer\n\n"
                   "1. Click to place the start node\n"
                   "2. Click to place the target node\n"
                   "3. Click/hold the mouse click to place barriers\n"
                   "4. Press SPACE to activate A* pathfinding algorithm or;\n"
                   "Press B to activate Breadth First Search algorithm\n"
                   "5. Press C to reset every node, press X to reset while keeping barriers\n\n"
                   "Also, hold right click to reset any nodes.\n")
    menu.add.button('Start', start)
    menu.mainloop(window)

    while True:
        continue


def main():
    pygame.init()
    pygame.mixer.init()
    # Initialize Pygame mixer
    # pygame.mixer.init(frequency=44100, size=-16, channels=2)
    window = pygame.display.set_mode((windowWidth, windowHeight))
    # pygame.mixer.init()
    # pygame.mixer.music.load(sound)
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")
    window.fill(BLACK)  # Black background acts as "outline" for the nodes
    grid = draw_grid(window)

    start = None
    target = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # Allows quiting while in the while loop
                return

            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # Left mouse click, set nodes to start, target, or barrier
                coord = pygame.mouse.get_pos()
                row, column = coord_to_grid(coord)

                node = grid[column][row]

                if not start and node is not target and node.check_state() == "walkable":
                    node.set_color(PURPLE)  # Start node
                    start = node
                    print("Start node set.")
                    time.sleep(0.1)

                elif not target and node is not start and node.check_state() == "walkable":
                    node.set_color(ORANGE)  # Target node
                    target = node
                    print("Target node set.")
                    time.sleep(0.1)

                elif node is not start and node is not target:
                    node.set_color(BLACK)  # Barrier node

                update_node(node, window)

            elif pygame.mouse.get_pressed(num_buttons=3)[2]:  # Right mouse click, reset clicked node to walkable
                coord = pygame.mouse.get_pos()
                row, column = coord_to_grid(coord)

                node = grid[column][row]
                node.set_color(WHITE)  # Walkable node color

                if node is start:
                    start = None
                elif node is target:
                    target = None

                update_node(node, window)

            elif e.type == pygame.KEYDOWN:

                if e.key == pygame.K_SPACE and start and target:  # A* algorithm
                    a_star_algo(start, target, grid, window)

                elif e.key == pygame.K_b and start and target:  # BFS algorithm
                    bfs_algo(start, target, grid, window)

                elif e.key == pygame.K_x and start and target:  # Reset but keep barriers, start node, and target node
                    reset_from_search(grid, window)

                elif e.key == pygame.K_c:  # Reset everything
                    start = None
                    target = None
                    grid = draw_grid(window)


if __name__ == '__main__':
    menu()
    main()
    pygame.quit()
