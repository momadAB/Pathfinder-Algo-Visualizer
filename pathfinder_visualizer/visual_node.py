import pygame
import ctypes
import pathfinder_visualizer
from pathfinder_visualizer import windowWidth, windowHeight

# Load kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Define Sleep function
usleep = kernel32.Sleep


class VisualNode:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = int(windowWidth / pathfinder_visualizer.GRID_X)
        self.height = int((windowHeight - pathfinder_visualizer.BlockSize) / pathfinder_visualizer.GRID_Y)
        self.color = pathfinder_visualizer.WHITE
        self.straight_neighbors = []
        self.diagonal_neighbors = []
        self.isClosed = False
        self.isOpen = False
        self.isBarrier = False
        self.parent = None
        self.hCost = 0
        self.gCost = 0
        self.border_radius = 0

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'isClosed': self.isClosed,
            'isOpen': self.isOpen,
            'isBarrier': self.isBarrier,
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
        if self.color == pathfinder_visualizer.LAVENDER \
                or self.color == pathfinder_visualizer.SLATE_GREY\
                or self.color == pathfinder_visualizer.WHITE\
                or self.color == pathfinder_visualizer.TEAL:
            return "walkable"
        elif self.color == pathfinder_visualizer.BLACK:
            return "barrier"
        elif self.color == pathfinder_visualizer.PURPLE:
            return "start"
        elif self.color == pathfinder_visualizer.ORANGE:
            return "target"

        else:
            return

    def draw(self, win):
        # Adjust the y position of the node
        rect_x = self.y * self.width
        rect_y = self.x * self.height + pathfinder_visualizer.BlockSize  # Apply the offset here
        self.rect = (rect_x, rect_y, self.width - 2, self.height - 2)
        pygame.draw.rect(win, self.color, self.rect, border_radius=0)
        pygame.display.update(self.rect)

    def draw_with_longer_animation(self, win):
        '''
        Same as draw() but with a 3 microsecond delay
        '''
        # Adjust the y position of the node
        rect_x = self.y * self.width
        rect_y = self.x * self.height + pathfinder_visualizer.BlockSize  # Apply the offset here
        self.rect = (rect_x, rect_y, self.width - 2, self.height - 2)
        pygame.draw.rect(win, self.color, self.rect, border_radius=0)
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
