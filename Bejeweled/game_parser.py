import argparse


class WrongBoardDimensions(Exception):
    def __init__(self, axis: str):
        """
        Raises exception when one of board dimension is below 8.

        Args:
            axis (str): width or height
        """
        super().__init__(f'The minimum of board {axis} is 8.')


class WrongNumberOfJewels(Exception):
    def __init__(self):
        """
        Raises exception when the number of jewels is below 6.
        """
        super().__init__('The number of jewels must be at least 6.')


class WrongNumberOfMoves(Exception):
    def __init__(self):
        """
        Raises exception when the number of moves is below 1.
        """
        super().__init__('The number of moves must me at least 1.')


class WrongGoalValue(Exception):
    def __init__(self):
        """
        Raises exception when the number of goal is below 100.
        """
        super().__init__('The basic goal must be at least 100.')


def create_parser(args):
    """
    Creates parser with argparse

    Args:
        args (list): list with arguments to be parsed

    Raises:
        WrongBoardDimensions: when -width below 6
        WrongBoardDimensions: when -height below 6
        WrongNumberOfJewels: when -jewel below 6
        WrongNumberOfMoves: when -move below 1
        WrongGoalValue: when -goal below 100

    Returns:
        argparse.Namespace: namespace object with attributes:
            width: board width
            height: board height
            jewel: number of jewels
            move: number of moves
            goal: basic goal
    """
    parser = argparse.ArgumentParser('Bejeweled game')
    parser.add_argument('-width', help='board width', type=int, default=8)
    parser.add_argument('-height', help='board height', type=int, default=8)
    parser.add_argument('-jewel', help='number of jewels', type=int, default=6)
    parser.add_argument('-move', help='number of moves', type=int, default=15)
    parser.add_argument('-goal', help='basic goal', type=int, default=800)
    arguments = parser.parse_args(args)
    if arguments.width < 8:
        raise WrongBoardDimensions('width')
    if arguments.height < 8:
        raise WrongBoardDimensions('height')
    if arguments.jewel < 6:
        raise WrongNumberOfJewels()
    if arguments.move < 1:
        raise WrongNumberOfMoves()
    if arguments.goal < 100:
        raise WrongGoalValue()
    return arguments
