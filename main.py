from bejeweled.interface import interface
from bejeweled.game import Game
from bejeweled.game_parser import create_parser
import sys


def main(args):
    """
    Parse arguments and loads leaderboard to Game class.
    Initialize game and shows the interface screen.

    Args:
        args (list): list with arguments to be parsed
    """
    arguments = create_parser(args)
    game = Game(arguments)
    game.leaderboard().load_from_file()
    interface(game)


if __name__ == '__main__':
    main(sys.argv[1:])
