# Pathfinder algorithm visualizer with A star algorithm and Breadth First Search algorithm
import time
import threading
import pygame
import pygame_menu
from pathlib import Path
import ctypes
from sound_player import play_sound_for_rect, create_sweep_sound

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


class VisualNode:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = int(windowWidth / GRID_X)
        self.height = int(windowHeight / GRID_Y)
        self.color = WHITE
        self.straight_neighbors = []
        self.diagonal_neighbors = []
        self.isClosed = False
        self.isOpen = False
        self.isBarrier = False
        self.parent = None
        self.hCost = 0
        self.gCost = 0

    def get_f_cost(self):
        return self.hCost + self.gCost

    def get_position(self):
        return self.x, self.y

    def set_color(self, color):
        self.color = color

    def check_state(self):

        if self.color == LAVENDER or self.color == SLATEGREY or self.color == WHITE or self.color == TEAL:
            return "walkable"
        elif self.color == BLACK:
            return "barrier"
        elif self.color == PURPLE:
            return "start"
        elif self.color == ORANGE:
            return "target"

        else:
            return

    def draw(self, win):
        self.rect = (self.y * self.width, self.x * self.height, self.width - 2, self.height - 2)
        # Rounded corners
        pygame.draw.rect(win, self.color, self.rect, border_radius=5)

        pygame.display.update(self.rect)

    def draw_with_longer_animation(self, win):
        # i = 1
        # while i < self.width - 1:
        #     for e in pygame.event.get():
        #         if e.type == pygame.QUIT:
        #             quit()
        #     self.rect = (self.y * self.width, self.x * self.height, i, i)
        #     pygame.draw.rect(win, self.color, self.rect, border_radius=5)
        #     pygame.display.update(self.rect)
        #     i += 1
        #     time.sleep(0.0001)
        self.rect = (self.y * self.width, self.x * self.height, self.width - 2, self.height - 2)
        # Rounded corners
        pygame.draw.rect(win, self.color, self.rect, border_radius=5)

        pygame.display.update(self.rect)

        # Microseconds sleep
        usleep(3)

    def get_neighbors(self, grid):
        self.straight_neighbors = []
        self.diagonal_neighbors = []
        rightOpen = False
        leftOpen = False
        upOpen = False
        downOpen = False

        # Straight Neighbors
        if self.y != GRID_X - 1:
            if grid[self.x][self.y + 1].check_state() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])
                rightOpen = True

        if self.y != 0:
            if grid[self.x][self.y - 1].check_state() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])
                leftOpen = True

        if self.x != GRID_Y - 1:
            if grid[self.x + 1][self.y].check_state() != "barrier":  # Down
                self.straight_neighbors.append(grid[self.x + 1][self.y])
                downOpen = True

        if self.y != 0:
            if grid[self.x - 1][self.y].check_state() != "barrier":  # Up
                self.straight_neighbors.append(grid[self.x - 1][self.y])
                upOpen = True

        # Diagonal Neighbors
        if upOpen and rightOpen:  # Top right
            self.diagonal_neighbors.append(grid[self.x - 1][self.y + 1])

        if upOpen and leftOpen:  # Top left
            self.diagonal_neighbors.append(grid[self.x - 1][self.y - 1])

        if downOpen and rightOpen:  # Bottom right
            self.diagonal_neighbors.append(grid[self.x + 1][self.y + 1])

        if downOpen and rightOpen:  # Bottom left
            self.diagonal_neighbors.append(grid[self.x + 1][self.y - 1])

        l = self.straight_neighbors
        l.extend(self.diagonal_neighbors)

        return l

    def get_neighbors_straight(self, grid):
        self.straight_neighbors = []

        # Straight Neighbors
        if self.y != GRID_X - 1:
            if grid[self.x][self.y + 1].check_state() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])

        if self.y != 0:
            if grid[self.x][self.y - 1].check_state() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])

        if self.x != GRID_Y - 1:
            if grid[self.x + 1][self.y].check_state() != "barrier":  # Down
                self.straight_neighbors.append(grid[self.x + 1][self.y])

        if self.y != 0:
            if grid[self.x - 1][self.y].check_state() != "barrier":  # Up
                self.straight_neighbors.append(grid[self.x - 1][self.y])

        l = self.straight_neighbors

        return l


# Reset every node except start, target, and barriers
def reset_from_search(grid, win):
    for row in grid:
        for node in row:
            if node.color == SLATEGREY or node.color == LAVENDER or node.color == TEAL:
                # node.set_color(WHITE)
                node.set_color(WHITE)
                update_node(node, win)


# # Retrace path from parents and color them maroon
# def retrace_path(self, window):
#     pathBack = []
#     if self.parent:
#
#         currentNode = self
#         i = 1
#         while currentNode:  # Traces back path from nodes parents, not including start and end nodes
#             for e in pygame.event.get():
#                 if e.type == pygame.QUIT:
#                     pygame.quit()
#             # pygame.mixer.Channel(i % 1).play(pygame.mixer.Sound(sound))
#             if currentNode.color is not ORANGE and currentNode.color is not PURPLE:
#                 currentNode.set_color(TEAL)
#                 # update_node_with_animation(currentNode, window)
#                 currentNode.draw(window)
#
#             currentNode = currentNode.parent
#             pathBack.append(currentNode)
#             i += 1
#
#     return pathBack

def retrace_path(self, window, duration=2.0):
    pathBack = []
    node_count = 0  # Initialize node counter

    # Count the nodes first
    currentNode = self
    while currentNode.parent:
        node_count += 1
        currentNode = currentNode.parent

    # Calculate the delay per node based on the duration and node count
    delay_per_node = duration / node_count if node_count else 0

    # Play the sweep sound based on the node count
    print(node_count, duration)
    sweep_sound = create_sweep_sound(node_count, duration)
    pygame.mixer.stop()
    sweep_sound.play()
    # pygame.time.wait(2000)  # Wait for 2 seconds
    #
    # test_sound = create_sweep_sound(10, 2)  # 10 nodes, 2 seconds duration
    # test_sound.play()
    # pygame.time.wait(2000)  # Wait for 2 seconds

    # Reset the current node to the end node
    currentNode = self

    while currentNode.parent:  # Retrace the path
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
        if currentNode.color not in [ORANGE, PURPLE]:
            currentNode.set_color(TEAL)
            currentNode.draw(window)
            pygame.display.flip()  # Update the display

        # Delay between each node
        pygame.time.wait(int(delay_per_node * 1000))

        currentNode = currentNode.parent
        pathBack.append(currentNode)

    # Wait for the sound to finish before exiting the function
    # (this may not be necessary if the drawing takes longer than the sound)
    remaining_sound_time = max(0, int(duration * 1000) - int(node_count * delay_per_node * 1000))
    pygame.time.wait(remaining_sound_time)

    return pathBack

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
            currentNode.set_color(SLATEGREY)
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
                    if neighbor is not startNode and neighbor.color is not SLATEGREY:
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
            currentNode.set_color(SLATEGREY)
            usleep(1)
            update_node(currentNode, window)

        for neighbor in currentNode.get_neighbors_straight(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")
                return retrace_path(neighbor, window)

            if neighbor.check_state() != "walkable":
                continue

            if neighbor is not startNode and neighbor.color is not SLATEGREY:
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


# Color constants
# WHITE = (215, 215, 215)
# BLACK = (54, 54, 54)
BLACK = (100, 100, 100)
WHITE = (54, 54, 54)
# DARK_GREEN = (64, 153, 87)
# GREEN = (96, 235, 131)
PURPLE = (209, 60, 232)
ORANGE = (230, 163, 69)
# MAROON = (128, 40, 40)
LAVENDER = (230, 230, 250)
SLATEGREY = (112, 128, 144)
# PURPLE = (104, 30, 116)
# ORANGE = (115, 81, 34)
TEAL = (50, 222, 170)


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
