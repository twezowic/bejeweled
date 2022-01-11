from colorsys import hls_to_rgb
from math import floor


def choose_colors(number_of_colors):
    colors = []
    for i in range(1, number_of_colors+1):
        h, l, s = (i/number_of_colors, 0.5, 1.0)
        r, g, b = [floor(255*i) for i in hls_to_rgb(h, l, s)]
        colors.append((r, g, b))
    return colors


board_width = 18  # min 8
board_height = 10  # min 8
SCREEN_WIDTH = board_width*50+110
SCREEN_HEIGHT = board_height*50+10
number_of_jewels = 6
number_of_moves = 15
basic_goal = 800
colors_of_jewels = choose_colors(number_of_jewels)
