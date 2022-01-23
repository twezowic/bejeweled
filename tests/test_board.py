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


def test_is_same_colour():
    jewel1 = Jewel('blue')
    jewel2 = Jewel('blue')
    assert jewel1.is_same_colour(jewel2)
    jewel3 = Jewel('white')
    jewel4 = Jewel('white')
    assert jewel3.is_same_colour(jewel4)


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
    table = [
        [Jewel('blue'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    assert board.destroying_move() is True


def test_not_destroing_move():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    assert board.destroying_move() is False


def test_swap_jewels():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    board.swap_jewels([0, 0], [1, 0])
    assert board.board() == [
        [Jewel('blue'), Jewel('red'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]


def test_falling_jewels():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('white'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    board.falling_jewels()
    assert_table = [
        [Jewel('red'), Jewel('white'), Jewel('blue')],
        [Jewel('blue'), Jewel('blue'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    for y in range(3):
        for x in range(3):
            assert board.board()[y][x].is_same_colour(assert_table[y][x])


def test_new_jewels():
    red = (255, 0, 0)
    table = [
        [Jewel(red), Jewel('white'), Jewel('white')],
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel(red)]
    ]
    board = Board(3, 3, 1, table)
    board.new_jewels()
    assert_table = [
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel(red)]
    ]
    for y in range(3):
        for x in range(3):
            assert board.board()[y][x].is_same_colour(assert_table[y][x])


def test_is_blank_with():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('white'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    assert board.is_blank() is True


def test_is_blank_without():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 3, table)
    assert board.is_blank() is False


def test_jewel_refill():
    red = (255, 0, 0)
    table = [
        [Jewel(red), Jewel('white'), Jewel('white')],
        [Jewel('white'), Jewel('white'), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel('white')]
    ]
    board = Board(3, 3, 1, table)
    board.jewel_refill()
    assert_table_1 = [
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel('white'), Jewel('white')],
        [Jewel(red), Jewel(red), Jewel(red)]
    ]
    for y in range(3):
        for x in range(3):
            assert board.board()[y][x].is_same_colour(assert_table_1[y][x])

    board.jewel_refill()
    assert_table_2 = [
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel(red)],
        [Jewel(red), Jewel(red), Jewel(red)]
    ]
    for y in range(3):
        for x in range(3):
            assert board.board()[y][x].is_same_colour(assert_table_2[y][x])


def test_game_over_blank():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('white'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is False


def test_game_over_possible_moves():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('green')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is False


def test_game_over_no_moves_left():
    table = [
        [Jewel('red'), Jewel('blue'), Jewel('blue')],
        [Jewel('blue'), Jewel('red'), Jewel('green')],
        [Jewel('green'), Jewel('red'), Jewel('green')]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over(True, 0) is True


def game_over_no_possible_move():
    table = [
        [Jewel('blue'), Jewel('blue'), Jewel('red')],
        [Jewel('green'), Jewel('red'), Jewel('green')],
        [Jewel('green'), Jewel('blue'), Jewel('green')]
    ]
    board = Board(3, 3, 1, table)
    assert board.game_over() is True
