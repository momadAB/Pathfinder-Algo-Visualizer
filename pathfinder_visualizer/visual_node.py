import pygame
import ctypes
import pathfinder_visualizer
from pathfinder_visualizer import windowWidth, windowHeight

# Load kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Define Sleep function
usleep = kernel32.Sleep

# Keep the ratio between the grids and window dimensions the same or there will be animation problems
# pathfinder_visualizer.GRID_X = 60
# pathfinder_visualizer.GRID_Y = 40

# windowHeight = 800
# windowWidth = 1200
# Color constants
BLACK = (100, 100, 100)
WHITE = (54, 54, 54)
PURPLE = (209, 60, 232)
ORANGE = (230, 163, 69)
LAVENDER = (230, 230, 250)
SLATE_GREY = (112, 128, 144)
TEAL = (50, 222, 170)


class VisualNode:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = int(windowWidth / pathfinder_visualizer.GRID_X)
        self.height = int(windowHeight / pathfinder_visualizer.GRID_Y)
        self.color = WHITE
        self.straight_neighbors = []
        self.diagonal_neighbors = []
        self.isClosed = False
        self.isOpen = False
        self.isBarrier = False
        self.parent = None
        self.hCost = 0
        self.gCost = 0

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'straightNeighbors': self.straight_neighbors,
            'diagonalNeighbors': self.diagonal_neighbors,
            'isClosed': self.isClosed,
            'isOpen': self.isOpen,
            'isBarrier': self.isBarrier,
            'parent': self.parent,
            'hCost': self.hCost,
            'gCost': self.gCost,
            }

    def get_f_cost(self):
        return self.hCost + self.gCost

    def get_position(self):
        return self.x, self.y

    def set_color(self, color):
        self.color = color

    def check_state(self):
        '''
        Checks the state of the node. Can be walkable, barrier, start, or target.
        :return:  String describing the state of the node
        '''
        if self.color == LAVENDER or self.color == SLATE_GREY or self.color == WHITE or self.color == TEAL:
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
        '''
        Same as draw() but with a 3 microsecond delay
        '''
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
        if self.y != pathfinder_visualizer.GRID_X - 1:
            if grid[self.x][self.y + 1].check_state() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])
                rightOpen = True

        if self.y != 0:
            if grid[self.x][self.y - 1].check_state() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])
                leftOpen = True

        if self.x != pathfinder_visualizer.GRID_Y - 1:
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
        if self.y != pathfinder_visualizer.GRID_X - 1:
            if grid[self.x][self.y + 1].check_state() != "barrier":  # Right
                self.straight_neighbors.append(grid[self.x][self.y + 1])

        if self.y != 0:
            if grid[self.x][self.y - 1].check_state() != "barrier":  # Left
                self.straight_neighbors.append(grid[self.x][self.y - 1])

        if self.x != pathfinder_visualizer.GRID_Y - 1:
            if grid[self.x + 1][self.y].check_state() != "barrier":  # Down
                self.straight_neighbors.append(grid[self.x + 1][self.y])

        if self.y != 0:
            if grid[self.x - 1][self.y].check_state() != "barrier":  # Up
                self.straight_neighbors.append(grid[self.x - 1][self.y])

        l = self.straight_neighbors

        return l
