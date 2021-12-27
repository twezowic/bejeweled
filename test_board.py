from numpy import array
from board import Board


def test_create_empty_board():
    board = Board()
    assert board.board().isinstance(array())
