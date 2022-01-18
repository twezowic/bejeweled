import argparse


class WrongBoardDimensions(Exception):
    def __init__(self, axis):
        super().__init__(f'The minimum of board {axis} is 8.')


class WrongNumberOfJewels(Exception):
    def __init__(self):
        super().__init__('The number of jewels must be at least 6.')


class WrongNumberOfMoves(Exception):
    def __init__(self):
        super().__init__('The number of moves must me at least 1.')


class WrongGoalValue(Exception):
    def __init__(self):
        super().__init__('The basic goal must be at least 100.')


def create_parser(args):
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
