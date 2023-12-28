# Pathfinder algorithm visualizer with A star algorithm and Breadth First Search algorithm
import threading
import pygame
import random
import pygame_menu
import time
import json
from pathlib import Path
import ctypes
import pathfinder_visualizer
from .sound_player import play_sound_for_rect
from .visual_node import VisualNode
from pathfinder_visualizer import windowWidth, windowHeight, switch_preset

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
# # Keep the ratio between the grids and window dimensions the same or there will be animation problems
# pathfinder_visualizer.GRID_X = 120
# pathfinder_visualizer.GRID_Y = 80

# Global volume variable
global_volume = 1.0


def main():
    pygame.init()
    pygame.mixer.init()
    # Initialize Pygame mixer
    # pygame.mixer.init(frequency=44100, size=-16, channels=2)
    window = pygame.display.set_mode((windowWidth, windowHeight))
    # pygame.mixer.init()
    # pygame.mixer.music.load(sound)
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")
    window.fill(pathfinder_visualizer.BACKGROUND)  # Black background acts as "outline" for the nodes

    # Create a font object
    # font = pygame.font.SysFont(None, 36)  # You can replace None with a font name

    # Render the text
    # text = font.render('Welcome', True, (255, 255, 255))  # White color

    # Fill the background
    top_bar_rect = pygame.Rect(0, 0, windowWidth, pathfinder_visualizer.BlockSize)
    pygame.draw.rect(window, pathfinder_visualizer.WHITE, top_bar_rect)

    # Blit the text
    # window.blit(text, (10, 10))

    grid = draw_grid(window)

    start = None
    target = None

    try:
        loaded_grid, gridx, gridy, start, target = load_grid_from_file('menugrid')
        if gridx == pathfinder_visualizer.GRID_X and gridy == pathfinder_visualizer.GRID_Y \
                and loaded_grid is not None:
            grid = loaded_grid
            redraw_grid(window, loaded_grid)
            print('loaded')
        else:
            start = None
            target = None
    except FileNotFoundError:
        print('no such file or directory')
        start = None
        target = None
        pass

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return  # Exit the loop if window is closed

            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # Left mouse click, set nodes to start, target, or barrier
                coord = pygame.mouse.get_pos()
                row, column = coord_to_grid(coord)

                node = grid[column][row]

                # print(start, target, node, node.check_state(), node.color)

                if not start and node is not target and node.check_state() == "walkable":
                    node.set_color(pathfinder_visualizer.PURPLE)  # Start node
                    start = node
                    print("Start node set.")
                    time.sleep(0.1)

                elif not target and node is not start and node.check_state() == "walkable":
                    node.set_color(pathfinder_visualizer.ORANGE)  # Target node
                    target = node
                    print("Target node set.")
                    time.sleep(0.1)

                elif node is not start and node is not target:
                    node.set_color(pathfinder_visualizer.BLACK)  # Barrier node

                update_node(node, window)

            elif pygame.mouse.get_pressed(num_buttons=3)[2]:  # Right mouse click, reset clicked node to walkable
                coord = pygame.mouse.get_pos()
                row, column = coord_to_grid(coord)

                # print(start, target, node.check_state(), node.color)

                node = grid[column][row]
                node.set_color(pathfinder_visualizer.WHITE)  # Walkable node color

                if node is start:
                    start = None
                elif node is target:
                    target = None

                update_node(node, window)

            elif e.type == pygame.KEYDOWN:

                if e.key == pygame.K_ESCAPE:
                    print('saved')
                    reset_from_search(grid, window)
                    save_grid_to_file(grid, pathfinder_visualizer.GRID_X,
                                      pathfinder_visualizer.GRID_Y, 'menugrid')
                    return  # Exit the loop if Escape is pressed

                elif e.key == pygame.K_SPACE and start and target:  # A* algorithm
                    a_star_algo(start, target, grid, window)

                elif e.key == pygame.K_s:
                    print('Saved layout to file')
                    save_grid_to_file(grid, pathfinder_visualizer.GRID_X,
                                      pathfinder_visualizer.GRID_Y, 'testfile')

                elif e.key == pygame.K_g:
                    reset_from_search(grid, window)
                    switch_preset('GREEN')
                    reset_start_and_target_colors(start, target, window)

                elif e.key == pygame.K_r:
                    reset_from_search(grid, window)
                    switch_preset('DARKRED')
                    reset_start_and_target_colors(start, target, window)

                elif e.key == pygame.K_l:
                    print('Loading layout')
                    loaded_grid, pathfinder_visualizer.GRID_X, pathfinder_visualizer.GRID_Y, \
                        start, target = load_grid_from_file('testfile')
                    if loaded_grid is not None:
                        grid = loaded_grid
                        redraw_grid(window, loaded_grid)

                elif e.key == pygame.K_b and start and target:  # BFS algorithm
                    bfs_algo(start, target, grid, window)

                elif e.key == pygame.K_x and start and target:  # Reset but keep barriers, start node, and target node
                    reset_from_search(grid, window)

                elif e.key == pygame.K_c:  # Reset everything
                    start = None
                    target = None
                    grid = draw_grid(window)


# Start menu of the program which tells the user how to use the program
def menu():
    pygame.init()

    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")

    # Calculate relative font sizes based on window dimensions
    title_font_size = max(5, windowWidth // 25)  # Title font size (5 is minimum)
    widget_font_size = max(5, windowWidth // 35)  # Widget font size (5 is minimum)
    key_font_size = max(5, windowWidth // 40)  # Key font size

    # Custom theme
    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),  # Transparent background
        title_font=pygame_menu.font.FONT_NEVIS,  # Custom font for title
        title_font_size=30,
        widget_font=pygame_menu.font.FONT_FRANCHISE,
        widget_font_size=20,
        widget_font_color=(255, 255, 255),
        selection_color=(255, 0, 0),
    )

    # Create Menu
    menu = pygame_menu.Menu('PATHFINDER VISUALIZER by Mohammad Baqer', windowWidth, windowHeight, theme=mytheme)

    def start():
        menu.close()
        main()  # Make sure to define the main function

    def change_volume(volume):
        global global_volume
        global_volume = volume  # Update the global volume

    def change_grid_size(value):
        pathfinder_visualizer.GRID_X = int(pathfinder_visualizer.GRID_X * value)  # Update the global grid_size
        pathfinder_visualizer.GRID_Y = int(pathfinder_visualizer.GRID_Y * value)

    def reset_slider():
        grid_size_slider.set_value(1.0)
        change_grid_size(1.0)

    # Add widgets
    menu.add.label("Steps to using Pathfinder Visualizer:", max_char=-1, font_size=title_font_size)
    menu.add.label("1. Click to place the start node\n"
                   "2. Click to place the target node\n"
                   "3. Click/hold to place barriers\n"
                   "4. Press SPACE for A* algorithm, B for BFS\n"
                   "5. Press C to reset, X to reset but keep barriers\n"
                   "Hold right click to erase.\n", max_char=-1, font_size=widget_font_size)
    # Add widgets
    menu.add.label("Adjust Volume")
    menu.add.range_slider('Volume', default=0.20, range_values=(0, 1), increment=0.1, onchange=change_volume)
    # Add Grid Size Slider
    menu.add.label("Adjust Grid Size")
    grid_size_slider = menu.add.range_slider('Grid Size', default=1.0, range_values=(0.5, 2.5), increment=0.1,
                                             onchange=change_grid_size)

    # Add a button to reset the grid size slider
    menu.add.button('Reset Grid Size', reset_slider)

    menu.add.button('Start', start)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Main loop
    while True:
        # Always make sure that the grid size is what the slider says. This avoids discrepancies after loading a map
        change_grid_size(grid_size_slider.get_value())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        window.fill((40, 40, 40))  # Fill background color
        menu.update(events)
        menu.draw(window)

        # Highlight keys
        key_instructions = [
            ("SPACE", "for A* algorithm"),
            ("B", "for BFS"),
            ("C", "to reset"),
            ("X", "to reset but keep barriers"),
            ("S", "to save current map"),
            ("L", "to load last saved map"),
            ("ESC", "to return to menu")
        ]
        x, y = 50, 210  # Starting position for key instructions
        for key, text in key_instructions:
            # Render key in red box
            key_surf = pygame.font.Font(None, key_font_size).render(key, True, pygame.Color('white'))
            key_rect = key_surf.get_rect(topleft=(x, y))
            pygame.draw.rect(window, (255, 0, 0), key_rect.inflate(10, 10), 0)
            window.blit(key_surf, key_rect)

            # Render accompanying text
            text_surf = pygame.font.Font(None, widget_font_size).render(text, True, pygame.Color('white'))
            window.blit(text_surf, (x + key_rect.width + 15, y))

            y += key_rect.height + 20  # Move down for the next instruction

        pygame.display.update()


def reset_start_and_target_colors(start, target, win):
    start.color = pathfinder_visualizer.PURPLE
    target.color = pathfinder_visualizer.ORANGE
    start.draw(win)
    target.draw(win)


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
            if node.color == pathfinder_visualizer.SLATE_GREY \
                    or node.color == pathfinder_visualizer.LAVENDER \
                    or node.color == pathfinder_visualizer.TEAL:
                # node.set_color(WHITE)
                node.set_color(pathfinder_visualizer.WHITE)
                update_node(node, win)


def retrace_path(self, window, duration=1.0):
    path_back = []
    if self.parent:
        current_node = self
        while current_node.parent:  # Traces back path from nodes parents, not including start and end nodes
            path_back.append(current_node)
            current_node = current_node.parent

        # print(path_back)
        # Randomly shuffle the path nodes, excluding the starting node (which is the last one in path_back)
        # random.shuffle(path_back)
        node_count = len(path_back)
        path_back = reversed(path_back)
        delay_per_node = duration / node_count if node_count else 0
        # print(path_back)

        # Draw the nodes in the start-to-end direction
        for node in path_back:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
            if node.color != pathfinder_visualizer.ORANGE \
                    and node.color != pathfinder_visualizer.PURPLE:
                node.set_color(pathfinder_visualizer.TEAL)
                pygame.time.wait(int(delay_per_node * 1000))
                # print(global_volume)
                # pygame.mixer.stop()
                play_sound_for_rect(node, pathfinder_visualizer.GRID_X, pathfinder_visualizer.GRID_Y, global_volume)
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
        for event in pygame.event.get():  # Check for pygame events
            if event.type == pygame.QUIT:  # Quit if window is closed
                return []
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Check for ESC key
                print("Search stopped by user")
                reset_from_search(grid, window)
                return []
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
            currentNode.set_color(pathfinder_visualizer.SLATE_GREY)
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
                    if neighbor is not startNode \
                            and neighbor.color is not pathfinder_visualizer.SLATE_GREY:
                        # pygame.mixer.music.play()
                        # pygame.mixer.stop()
                        play_sound_for_rect(neighbor, pathfinder_visualizer.GRID_X, pathfinder_visualizer.GRID_Y,
                                            global_volume)
                        neighbor.set_color(pathfinder_visualizer.LAVENDER)
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
        for event in pygame.event.get():  # Check for pygame events
            if event.type == pygame.QUIT:  # Quit if window is closed
                return []
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Check for ESC key
                print("Search stopped by user")
                reset_from_search(grid, window)
                return []
        currentNode = queue.pop(0)

        if currentNode is not startNode:
            # pygame.mixer.music.play()
            currentNode.set_color(pathfinder_visualizer.SLATE_GREY)
            usleep(1)
            # pygame.mixer.stop()
            play_sound_for_rect(neighbor, pathfinder_visualizer.GRID_X, pathfinder_visualizer.GRID_Y, global_volume)
            update_node(currentNode, window)

        for neighbor in currentNode.get_neighbors_straight(grid):

            if neighbor is targetNode:
                neighbor.parent = currentNode
                print("Path found")
                return retrace_path(neighbor, window)

            if neighbor.check_state() != "walkable":
                continue

            if neighbor is not startNode \
                    and neighbor.color is not pathfinder_visualizer.SLATE_GREY:
                # pygame.mixer.music.play()
                neighbor.set_color(pathfinder_visualizer.LAVENDER)
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

    column = x // (windowWidth // pathfinder_visualizer.GRID_X)
    if y > pathfinder_visualizer.BlockSize:
        row = ((y - pathfinder_visualizer.BlockSize) //
               ((windowHeight - pathfinder_visualizer.BlockSize) // pathfinder_visualizer.GRID_Y))
    else:
        row = 0
    # print(int((windowHeight - pathfinder_visualizer.BlockSize) / pathfinder_visualizer.GRID_Y), row)

    return column, row


def draw_grid(win):
    grid = []

    # Populate grid only once
    for i in range(pathfinder_visualizer.GRID_Y):
        grid.append([])
        for j in range(pathfinder_visualizer.GRID_X):
            node = VisualNode(i, j)
            grid[i].append(node)

    # Make outline - Check if the grid is non-empty and has enough rows
    if grid and len(grid) > pathfinder_visualizer.GRID_Y - 1:
        for node in grid[0]:
            node.set_color(pathfinder_visualizer.BLACK)
        for node in grid[-1]:
            node.set_color(pathfinder_visualizer.BLACK)

        # Make vertical outlines
        vertical1 = [row[0] for row in grid if row]  # First element of each row
        vertical2 = [row[-1] for row in grid if row]  # Last element of each row
        for node in vertical1 + vertical2:
            node.set_color(pathfinder_visualizer.BLACK)

    # Draw nodes in grid
    for row in grid:
        for node in row:
            node.draw(win)

    pygame.display.update()

    return grid


def redraw_grid(window, grid):
    """
    Redraws the entire grid on the given window.

    :param window: The graphical window where the grid is to be drawn.
    :param grid: The grid, a 2D list of VisualNode objects.
    """
    # Clear the window before redrawing
    window.fill(pathfinder_visualizer.BACKGROUND)

    top_bar_rect = pygame.Rect(0, 0, windowWidth, pathfinder_visualizer.BlockSize)
    pygame.draw.rect(window, pathfinder_visualizer.WHITE, top_bar_rect)

    # Draw each node in the grid
    for row in grid:
        for node in row:
            node.draw(window)

    # Update the display to show the new drawings
    pygame.display.update()


# Example usage
# redraw_grid(window, grid)


def save_grid_to_file(grid, grid_x, grid_y, filename):
    # Convert grid to a simpler representation
    simple_grid = [[node.to_dict() for node in row] for row in grid]

    # Create a dictionary to hold grid data and dimensions
    grid_data = {
        'grid': simple_grid,
        'GRID_X': grid_x,
        'GRID_Y': grid_y
    }

    # Write to a file
    with open(filename, 'w') as file:
        json.dump(grid_data, file, indent=4)


def load_grid_from_file(filename):
    try:
        with open(filename, 'r') as file:
            grid_data = json.load(file)

        grid_x = grid_data['GRID_X']
        grid_y = grid_data['GRID_Y']
        serialized_grid = grid_data['grid']

        # Create a grid of VisualNode objects
        grid = [[VisualNode(node_data['x'], node_data['y']) for node_data in row] for row in serialized_grid]

        startNode = None
        targetNode = None

        # Now populate the attributes of each node
        for i, row in enumerate(serialized_grid):
            for j, node_data in enumerate(row):
                node = grid[i][j]
                node.width = node_data['width']
                node.height = node_data['height']
                node.color = node_data['color']
                node.isClosed = node_data['isClosed']
                node.isOpen = node_data['isOpen']
                node.isBarrier = node_data['isBarrier']
                node.hCost = node_data['hCost']
                node.gCost = node_data['gCost']
                node.parent = []
                node.straight_neighbors = []
                node.diagonal_neighbors = []
                # For parent, straightNeighbors, and diagonalNeighbors, you need to reconstruct the references
                # This part is omitted for simplicity and needs to be implemented based on how these are stored

                # Identify start and target nodes
                node_state = node.check_state()
                if node_state == 'start':
                    startNode = node
                elif node_state == 'target':
                    targetNode = node

        return grid, grid_x, grid_y, startNode, targetNode
    except FileNotFoundError:
        print("File not found")
        return None, pathfinder_visualizer.GRID_X, pathfinder_visualizer.GRID_Y, None, None
