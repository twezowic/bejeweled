from bejeweled.game_parser import (
    create_parser,
    WrongBoardDimensions,
    WrongGoalValue,
    WrongNumberOfJewels,
    WrongNumberOfMoves
)
import pytest


def test_create_parser_default():
    arguments = create_parser([])
    assert arguments.width == 8
    assert arguments.height == 8
    assert arguments.jewel == 6
    assert arguments.move == 15
    assert arguments.goal == 800


def test_set_arguments_width():
    arguments = create_parser(['-width', '10'])
    assert arguments.width == 10


def test_set_arguments_height():
    arguments = create_parser(['-height', '10'])
    assert arguments.height == 10


def test_set_arguments_jewel():
    arguments = create_parser(['-jewel', '10'])
    assert arguments.jewel == 10


def test_set_arguments_move():
    arguments = create_parser(['-move', '10'])
    assert arguments.move == 10


def test_set_arguments_goal():
    arguments = create_parser(['-goal', '1000'])
    assert arguments.goal == 1000


def test_set_arguments_wrong_width():
    with pytest.raises(WrongBoardDimensions):
        create_parser(['-width', '0'])


def test_set_arguments_wrong_height():
    with pytest.raises(WrongBoardDimensions):
        create_parser(['-height', '0'])


def test_set_arguments_wrong_jewel():
    with pytest.raises(WrongNumberOfJewels):
        create_parser(['-jewel', '0'])


def test_set_arguments_wrong_move():
    with pytest.raises(WrongNumberOfMoves):
        create_parser(['-move', '0'])


def test_set_arguments_wrong_goal():
    with pytest.raises(WrongGoalValue):
        create_parser(['-goal', '3'])
