from interface import interface
from game import Game
from game_parser import create_parser
import sys


def main(args):
    arguments = create_parser(args)
    print(arguments)
    game = Game(arguments)
    game.leaderboard().load_from_file()
    interface(game)


if __name__ == '__main__':
    main(sys.argv[1:])
