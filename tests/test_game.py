from bejeweled.game import Level, Game, is_adjacent
from bejeweled.game_parser import create_parser
from bejeweled.leaderboard import Score
from bejeweled.board import Board, Jewel


def test_change_mode():
    level = Level(1000, 15)
    assert level.mode() == 'normal'
    level.change_mode()
    assert level.mode() == 'endless'


def test_is_normal():
    level = Level(1000, 15)
    assert level.is_normal() is True
    level.change_mode()
    assert level.is_normal() is False


def test_add_level():
    level = Level(1000, 15)
    assert level.level() == 1
    level.add_level()
    assert level.level() == 2


def test_set_goal():
    level = Level(1000, 15)
    level.add_goal()
    assert level.goal() == 1200


def test_one_move():
    level = Level(1000, 15)
    assert level.moves() == 15
    level.one_move()
    assert level.moves() == 14


def test_reset_moves():
    level = Level(1000, 15)
    for i in range(5):
        level.one_move()
    assert level.moves() == 10
    level.reset_moves(15)
    assert level.moves() == 15


def test_win_condtion():
    level = Level(1000, 15)
    assert level.win_condition(1000) is True


def test_win_condition_not_normal_mode():
    level = Level(1000, 15)
    level.change_mode()
    assert level.win_condition(1000) is False


def test_win_condition_not_enough():
    level = Level(1000, 15)
    assert level.win_condition(800) is False


def test_reset_level():
    arguments = create_parser([])
    game = Game(arguments)
    assert game.level().goal() == 800
    assert game.level().moves() == 15
    game.level().one_move()
    game.level().add_goal()
    assert game.level().goal() == 1000
    assert game.level().moves() == 14
    game.reset_level()
    assert game.level().goal() == 800
    assert game.level().moves() == 15


def test_set_new_score():
    arguments = create_parser([])
    game = Game(arguments)
    assert game.score().name() == ''
    assert game.score().score() == 0
    game.set_score(Score('bob', 100))
    assert game.score().name() == 'bob'
    assert game.score().score() == 100


def test_next_level():
    arguments = create_parser([])
    game = Game(arguments)
    game.level().one_move()
    game.set_score(Score('bob', 100))
    assert game.level().level() == 1
    assert game.level().goal() == 800
    assert game.level().moves() == 14
    assert game.score().score() == 100
    assert game.score().name() == 'bob'
    game.next_level()
    assert game.level().level() == 2
    assert game.level().goal() == 1000
    assert game.level().moves() == 15
    assert game.score().score() == 0
    assert game.score().name() == 'bob'


def test_adjacent_horiznotal():
    assert is_adjacent((0, 0), (0, 1)) is True


def test_adjacent_vertical():
    assert is_adjacent((3, 3), (4, 3)) is True


def test_no_adjacent():
    assert is_adjacent((3, 5), (0, 1)) is False


def test_is_match():
    arguments = create_parser([])
    game = Game(arguments)
    assert game._is_match(3, False) is True
    assert game._is_match(2, False) is False


def test_is_match_scores():
    arguments = create_parser([])
    game = Game(arguments)
    assert game.score().score() == 0
    game._is_match(3, True)
    assert game.score().score() == 100


def test_destroying_jewels():
    arguments = create_parser([])
    game = Game(arguments)
    game.set_board(Board(3, 3, 3, [
        [Jewel('red'), Jewel('red'), Jewel('green')],
        [Jewel('red'), Jewel('blue'), Jewel('red')],
        [Jewel('red'), Jewel('red'), Jewel('red')]
    ]))
    game.destroying_jewels(False)
    table = [
        [Jewel('white'), Jewel('red'), Jewel('green')],
        [Jewel('white'), Jewel('blue'), Jewel('red')],
        [Jewel('white'), Jewel('white'), Jewel('white')]
    ]
    for y in range(3):
        for x in range(3):
            assert game.board().board()[y][x].is_same_colour(table[y][x])
    assert game.score().score() == 0


def test_destorying_jewels_earning_points():
    arguments = create_parser([])
    game = Game(arguments)
    game.set_board(Board(3, 3, 3, [
        [Jewel('red'), Jewel('red'), Jewel('green')],
        [Jewel('red'), Jewel('blue'), Jewel('red')],
        [Jewel('red'), Jewel('red'), Jewel('red')]
    ]))
    game.destroying_jewels(True)
    table = [
        [Jewel('white'), Jewel('red'), Jewel('green')],
        [Jewel('white'), Jewel('blue'), Jewel('red')],
        [Jewel('white'), Jewel('white'), Jewel('white')]
    ]
    for y in range(3):
        for x in range(3):
            assert game.board().board()[y][x].is_same_colour(table[y][x])
    assert game.score().score() == 200


def test_destoring_jewels_blank():
    arguments = create_parser([])
    game = Game(arguments)
    game.set_board(Board(3, 3, 3, [
        [Jewel('white'), Jewel('red'), Jewel('green')],
        [Jewel('red'), Jewel('blue'), Jewel('red')],
        [Jewel('red'), Jewel('red'), Jewel('red')]
    ]))
    game.destroying_jewels(False)
    table = [
        [Jewel('white'), Jewel('red'), Jewel('green')],
        [Jewel('red'), Jewel('blue'), Jewel('red')],
        [Jewel('red'), Jewel('red'), Jewel('red')]
    ]
    for y in range(3):
        for x in range(3):
            assert game.board().board()[y][x].is_same_colour(table[y][x])
