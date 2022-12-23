# Pathfinder algorithm visualizer with A star algorithm and Breadth First Search algorithm
import time
import threading
import pygame
import pygame_menu
from pathlib import Path

sound = Path(__file__).with_name('button-6.wav')

sound2 = r"button-6.wav"
# Diagonal cost: approximation of sqrt(2), which would be the length of the hypotenuse of a right triangle of sides
# length 1
DIAGONAL_COST = 14
STRAIGHT_COST = 10
# Keep the ratio between the grids and window dimensions the same or there will be animation problems
GRID_X = 60
GRID_Y = 40
windowHeight = 800
windowWidth = 1200


# Calculates the overall cost
def getDistance(node1, node2):
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

    def getFCost(self):
        return self.hCost + self.gCost

    def getPosition(self):
        return self.x, self.y

    def setColor(self, color):
        self.color = color

    def checkState(self):

        if self.color == DARK_GREEN or self.color == GREEN or self.color == WHITE or self.color == MAROON:
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
        self.rect = pygame.draw.rect(win, self.color,
                                     (self.y * self.width, self.x * self.height, self.width - 2, self.width - 2))
        pygame.display.update(self.rect)

    def drawWithAnimationLonger(self, win):
        i = 1
        while i < self.width - 1:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
            self.rect = pygame.draw.rect(win, self.color, (self.y * self.width, self.x * self.height, i, i))
            pygame.display.update(self.rect)
            i += 1
            time.sleep(0.0001)

    def getNeighbors(self, grid):
        self.straight_neighbors = []
        self.diagonal_neighbors = []
        rightOpen = False
        leftOpen = False
        upOpen = False
        downOpen = False

        # Straight Neighbors
        if self.y != GRID_X - 1:
            if grid[self.x][self.y + 1].checkState() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])
                rightOpen = True

        if self.y != 0:
            if grid[self.x][self.y - 1].checkState() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])
                leftOpen = True

        if self.x != GRID_Y - 1:
            if grid[self.x + 1][self.y].checkState() != "barrier":  # Down
                self.straight_neighbors.append(grid[self.x + 1][self.y])
                downOpen = True

        if self.y != 0:
            if grid[self.x - 1][self.y].checkState() != "barrier":  # Up
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

    def getNeighborsStraight(self, grid):
        self.straight_neighbors = []

        # Straight Neighbors
        if self.y != GRID_X - 1:
            if grid[self.x][self.y + 1].checkState() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])

        if self.y != 0:
            if grid[self.x][self.y - 1].checkState() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])

        if self.x != GRID_Y - 1:
            if grid[self.x + 1][self.y].checkState() != "barrier":  # Down
                self.straight_neighbors.append(grid[self.x + 1][self.y])

        if self.y != 0:
            if grid[self.x - 1][self.y].checkState() != "barrier":  # Up
                self.straight_neighbors.append(grid[self.x - 1][self.y])

        l = self.straight_neighbors

        return l


# Reset every node except start, target, and barriers
def resetFromSearch(grid, win):
    for row in grid:
        for node in row:
            if node.color == GREEN or node.color == DARK_GREEN or node.color == MAROON:
                node.setColor(WHITE)
                updateNode(node, win)


# Retrace path from parents and color them maroon
def retracePath(self, window):
    pathBack = []
    if self.parent:

        currentNode = self
        i = 1
        while currentNode:  # Traces back path from nodes parents, not including start and end nodes
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
            pygame.mixer.Channel(i % 1).play(pygame.mixer.Sound(sound))
            if currentNode.color is not ORANGE and currentNode.color is not PURPLE:
                currentNode.setColor(MAROON)
                updateNodeWithAnimation(currentNode, window)

            currentNode = currentNode.parent
            pathBack.append(currentNode)
            i += 1

    return pathBack


# A* pathfinding algorithm
def astarAlgo(startNode, targetNode, grid, window):
    openSet = []
    closedSet = []
    startNode.gCost = 0
    targetNode.gCost = 0
    startNode.hCost = getDistance(startNode, targetNode)
    targetNode.hCost = 0

    openSet.append(startNode)
    i = 1
    while openSet:
        currentNode = openSet[0]

        for node in openSet:
            if node == openSet[0]:
                continue
            if node.getFCost() < currentNode.getFCost() or (
                    node.getFCost() == currentNode.getFCost() and node.hCost < currentNode.hCost):
                currentNode = node

        openSet.remove(currentNode)
        closedSet.append(currentNode)

        if currentNode is not startNode:
            currentNode.setColor(GREEN)
            updateNode(currentNode, window)

        for neighbor in currentNode.getNeighbors(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")
                return retracePath(neighbor, window)

            if neighbor.checkState() != "walkable" or neighbor in closedSet:
                continue

            costToNeighbor = currentNode.gCost + getDistance(currentNode, neighbor)
            if costToNeighbor < neighbor.gCost or neighbor not in openSet:
                neighbor.gCost = costToNeighbor
                neighbor.hCost = getDistance(neighbor, targetNode)
                neighbor.parent = currentNode

                if neighbor not in openSet:
                    openSet.append(neighbor)
                    if neighbor is not startNode and neighbor.color is not GREEN:
                        pygame.mixer.music.play()
                        neighbor.setColor(DARK_GREEN)
                        updateNode(neighbor, window)

    print("Path not found")
    return []


# Breadth First Search pathfinding algorithm
def bfsAlgo(startNode, targetNode, grid, window):
    visited = []
    queue = []
    visited.append(startNode)
    queue.append(startNode)

    while queue:
        currentNode = queue.pop(0)

        if currentNode is not startNode:
            pygame.mixer.music.play()
            currentNode.setColor(GREEN)
            updateNode(currentNode, window)

        for neighbor in currentNode.getNeighborsStraight(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")
                return retracePath(neighbor, window)

            if neighbor.checkState() != "walkable":
                continue

            if neighbor is not startNode and neighbor.color is not GREEN:
                pygame.mixer.music.play()
                neighbor.setColor(DARK_GREEN)
                updateNode(neighbor, window)

            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                neighbor.parent = currentNode


# Update visuals of node
def updateNode(node, window):
    node.draw(window)
    pygame.display.update(node.rect)


# Update visuals of node with an animation and threading
def updateNodeWithAnimation(node, window):
    d = threading.Thread(target=node.drawWithAnimationLonger(window))
    d.start()
    pygame.display.update(node.rect)


# Convert x, y coordinates into grid values
def coordToGrid(coord):
    x, y = coord

    column = x // (windowWidth // GRID_X)
    row = y // (windowHeight // GRID_Y)

    return column, row


def drawGrid(win):
    grid = []
    # Populate grid
    for i in range(GRID_Y):
        grid.append([])
        for j in range(GRID_X):
            node = VisualNode(i, j)
            grid[i].append(node)

    # Make outline
    for node in grid[0]:
        node.setColor(BLACK)
    for node in grid[GRID_Y - 1]:
        node.setColor(BLACK)
    vertical1 = []
    vertical2 = []
    for list in grid:
        vertical1.append(list[0])
        vertical2.append(list[GRID_X - 1])
    for node in vertical1:
        node.setColor(BLACK)
    for node in vertical2:
        node.setColor(BLACK)

    # Draw nodes in grid
    for row in grid:
        for node in row:
            node.draw(win)

    pygame.display.update()

    return grid

# Color constants
WHITE = (215, 215, 215)
BLACK = (54, 54, 54)
DARK_GREEN = (64, 153, 87)
GREEN = (96, 235, 131)
PURPLE = (209, 60, 232)
ORANGE = (230, 163, 69)
MAROON = (128, 40, 40)


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
    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")
    window.fill(BLACK)  # Black background acts as "outline" for the nodes
    grid = drawGrid(window)

    start = None
    target = None

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # Allows quiting while in the while loop
                return

            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # Left mouse click, set nodes to start, target, or barrier
                coord = pygame.mouse.get_pos()
                row, column = coordToGrid(coord)

                node = grid[column][row]

                if not start and node is not target and node.checkState() == "walkable":
                    node.setColor(PURPLE)  # Start node
                    start = node
                    print("Start node set.")
                    time.sleep(0.1)

                elif not target and node is not start and node.checkState() == "walkable":
                    node.setColor(ORANGE)  # Target node
                    target = node
                    print("Target node set.")
                    time.sleep(0.1)

                elif node is not start and node is not target:
                    node.setColor(BLACK)  # Barrier node

                updateNode(node, window)

            elif pygame.mouse.get_pressed(num_buttons=3)[2]:  # Right mouse click, reset clicked node to walkable
                coord = pygame.mouse.get_pos()
                row, column = coordToGrid(coord)

                node = grid[column][row]
                node.setColor(WHITE)  # Walkable node color

                if node is start:
                    start = None
                elif node is target:
                    target = None

                updateNode(node, window)

            elif e.type == pygame.KEYDOWN:

                if e.key == pygame.K_SPACE and start and target:  # A* algorithm
                    astarAlgo(start, target, grid, window)

                elif e.key == pygame.K_b and start and target:  # BFS algorithm
                    bfsAlgo(start, target, grid, window)

                elif e.key == pygame.K_x and start and target:  # Reset but keep barriers, start node, and target node
                    resetFromSearch(grid, window)

                elif e.key == pygame.K_c:  # Reset everything
                    start = None
                    target = None
                    grid = drawGrid(window)


if __name__ == '__main__':
    menu()
    main()
    pygame.quit()
