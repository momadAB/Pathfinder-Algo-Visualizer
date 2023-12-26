# Pathfinder algorithm visualizer with A star algorithm and Breadth First Search algorithm
import pygame_menu
import time
from pathfinder_visualizer.utilities import *


# Start menu of the program which tells the user how to use the program
def menu():
    pygame.init()

    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Pathfinder Visualizer by Mohammad Baqer")

    # Calculate relative font sizes based on window dimensions
    title_font_size = max(5, windowWidth // 25)  # Title font size (5 is minimum)
    widget_font_size = max(5, windowWidth // 35)  # Widget font size (5 is minimum)

    # Custom theme
    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),  # Transparent background
        title_font=pygame_menu.font.FONT_NEVIS,  # Custom font for title
        title_font_size=30,
        widget_font=pygame_menu.font.FONT_FRANCHISE,
        widget_font_size=20,
        widget_font_color=(255, 255, 255),
        selection_color=(255, 0, 0)
    )

    # Create Menu
    menu = pygame_menu.Menu('PATHFINDER VISUALIZER by Mohammad Baqer', windowWidth, windowHeight, theme=mytheme)

    def start():
        menu.close()
        main()  # Make sure to define the main function

    def change_volume(volume):
        global global_volume
        global_volume = volume  # Update the global volume

    # Add widgets
    menu.add.label("Steps to using Pathfinder Visualizer:", max_char=-1, font_size=title_font_size)
    menu.add.label("1. Click to place the start node\n"
                   "2. Click to place the target node\n"
                   "3. Click/hold to place barriers\n"
                   "4. Press SPACE for A* algorithm, B for BFS\n"
                   "5. Press C to reset, X to keep barriers\n"
                   "Hold right click to reset nodes.\n", max_char=-1, font_size=widget_font_size)
    # Add widgets
    menu.add.label("Adjust Volume")
    menu.add.range_slider('Volume', default=1, range_values=(0, 1), increment=0.1, onchange=change_volume)
    menu.add.button('Start', start)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Main loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        window.fill((40, 40, 40))  # Fill background color
        menu.update(events)
        menu.draw(window)

        pygame.display.update()


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
            if e.type == pygame.QUIT:
                return  # Exit the loop if window is closed
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return  # Exit the loop if Escape is pressed

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
