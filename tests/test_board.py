from bejeweled.board import _choose_colors, Jewel, Board


def test_choose_colors():
    chosed_colors = _choose_colors(3)
    rgb = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for colour in rgb:
        assert colour in chosed_colors


def test_set_colour():
    jewel = Jewel((0, 255, 0))
    assert jewel.colour() == (0, 255, 0)
    jewel.set_colour((255, 0, 0))
    assert jewel.colour() == (255, 0, 0)


def test_set_to_delete():
    jewel = Jewel((0, 255, 0))
    jewel.set_delete(True)
    assert jewel.delete() is True


def test_eq():
    jewel1 = Jewel('blue')
    jewel2 = Jewel('blue')
    assert jewel1 == jewel2


def test_eq_white():
    jewel1 = Jewel('white')
    jewel2 = Jewel('white')
    assert jewel1 != jewel2


def test_board_init():
    board = Board(8, 10, 3)
    assert board.width() == 8
    assert board.height() == 10
    rgb = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for colour in rgb:
        assert colour in board.colors()


def test_create_board():
    board = Board(8, 8, 1)
    colour = (255, 0, 0)
    board.create_board()
    for y in range(board.height()):
        for x in range(board.width()):
            assert board.board()[y][x].colour() == colour


def test_destroying_move():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_blue, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    assert board.destroying_move() is True


def test_not_destroing_move():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    assert board.destroying_move() is False


def test_swap_jewels():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    board.swap_jewels([0, 0], [1, 0])
    assert board.board() == [
        [jewel_blue, jewel_red, jewel_blue],
        [jewel_blue, jewel_red, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]


def test_falling_jewels():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    jewel_blank = Jewel('white')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_blank, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    board.falling_jewels()
    assert board.board() == [
        [jewel_red, jewel_blank, jewel_blue],
        [jewel_blue, jewel_blue, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]


def test_new_jewels():
    jewel_red = Jewel((255, 0, 0))
    jewel_blank = Jewel('white')
    table = [
        [jewel_red, jewel_blank, jewel_blank],
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_red, jewel_red]
    ]
    board = Board(3, 3, 1, table)
    board.new_jewels()
    assert board.board() == [
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_red, jewel_red]
    ]


def test_is_blank_with():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    jewel_blank = Jewel('white')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_blank, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    assert board.is_blank() is True


def test_is_blank_without():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 3, table)
    assert board.is_blank() is False


def test_jewel_refill():
    jewel_red = Jewel((255, 0, 0))
    jewel_blank = Jewel('white')
    table = [
        [jewel_red, jewel_blank, jewel_blank],
        [jewel_blank, jewel_blank, jewel_red],
        [jewel_red, jewel_red, jewel_blank]
    ]
    board = Board(3, 3, 1, table)
    board.jewel_refill()
    assert board.board() == [
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_blank, jewel_blank],
        [jewel_red, jewel_red, jewel_red]
    ]
    board.jewel_refill()
    assert board.board() == [
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_red, jewel_red],
        [jewel_red, jewel_red, jewel_red]
    ]


def test_game_over_blank():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    jewel_blank = Jewel('white')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_blank, jewel_red],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is False


def test_game_over_possible_moves():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_green],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is False


def test_game_over_no_moves_left():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_red, jewel_blue, jewel_blue],
        [jewel_blue, jewel_red, jewel_green],
        [jewel_green, jewel_red, jewel_green]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over(True, 0) is True


def game_over_no_possible_move():
    jewel_blue = Jewel('blue')
    jewel_red = Jewel('red')
    jewel_green = Jewel('green')
    table = [
        [jewel_blue, jewel_blue, jewel_red],
        [jewel_green, jewel_red, jewel_green],
        [jewel_green, jewel_blue, jewel_green]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is True
