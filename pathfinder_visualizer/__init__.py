# Keep the ratio between the grids and window dimensions the same or there will be animation problems
GRID_X = 60  # 15 - 150
GRID_Y = 40  # 10 - 100

windowHeight = 800
windowWidth = 1200

# Color presets
# BLACK is empty node, WHITE is barrier
# PURPLE is start node, ORANGE is end node
# LAVENDER is edge search nodes, SLATE_GREY is searched nodes
# TEAL is path to end node

BACKGROUND = [80, 80, 80]
BLACK = [70, 70, 70]
WHITE = [54, 54, 54]
# PURPLE = [209, 60, 232]
# PURPLE = [43, 222, 148]
# # ORANGE = [230, 163, 69]
# ORANGE = [97, 201, 103]
# # LAVENDER = [230, 230, 250]
# LAVENDER = [155, 185, 158]
# # SLATE_GREY = [112, 128, 144]
# SLATE_GREY = [83, 120, 56]
# # TEAL = [50, 222, 170]
# TEAL = [0, 230, 0]

# GREEN PRESET
PURPLE = [43, 222, 148]
ORANGE = [97, 201, 103]
LAVENDER = [155, 185, 158]
SLATE_GREY = [109, 158, 74]
# TEAL = [0, 230, 0]  # Green
# TEAL = [224, 217, 0]  # Yellow
TEAL = [222, 148, 43]  # Orange


def green_preset():
    # GREEN PRESET
    global PURPLE, ORANGE, LAVENDER, SLATE_GREY, TEAL
    PURPLE = [43, 222, 148]
    ORANGE = [97, 201, 103]
    LAVENDER = [155, 185, 158]
    SLATE_GREY = [109, 158, 74]
    TEAL = [222, 148, 43]  # Orange


def dark_red_preset():
    # DARK RED PRESET
    global PURPLE, ORANGE, LAVENDER, SLATE_GREY, TEAL
    PURPLE = [43, 0, 0]
    ORANGE = [97, 0, 0]
    LAVENDER = [155, 0, 0]
    SLATE_GREY = [83, 0, 0]
    TEAL = [230, 0, 0]


def light_red_preset():
    # LIGHT RED PRESET
    global PURPLE, ORANGE, LAVENDER, SLATE_GREY, TEAL
    PURPLE = [50, 0, 0]
    ORANGE = [124, 0, 0]
    LAVENDER = [120, 55, 55]
    SLATE_GREY = [140, 96, 96]
    TEAL = [230, 0, 0]


SWITCH_DICT = { 'GREEN': green_preset,
                "DARKRED": dark_red_preset,
                'LIGHTRED': light_red_preset
                }


def switch_preset(preset_name):
    '''
    Switches the color preset
    :param preset_name: Can be GREEN, DARKRED, or LIGHTRED
    '''
    SWITCH_DICT.get(preset_name, green_preset)()
