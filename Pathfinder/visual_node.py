import pygame
import ctypes

# Load kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Define Sleep function
usleep = kernel32.Sleep

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
