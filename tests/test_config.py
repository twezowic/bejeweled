from Bejeweled.config import choose_colors


def test_choose_colors():
    colors = choose_colors(3)

    rgb = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for i in range(3):
        assert rgb[i] in colors
