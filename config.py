from colorsys import hls_to_rgb
from math import floor

board_width = 20  # min 3
board_height = 8  # min 3
number_of_jewels = 5

def choose_colors(number_of_colors):
    colors = []
    for i in range(1, number_of_colors+1):
        h, l, s = (i/number_of_colors, 0.5, 1.0)
        r, g, b = [floor(255*i) for i in hls_to_rgb(h, l, s)]
        colors.append((r, g, b))
    return colors

colors_of_jewels = choose_colors(number_of_jewels)