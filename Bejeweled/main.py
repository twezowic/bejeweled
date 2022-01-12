from interface import interface
from game import Game


def main():
    game = Game()
    game.setup()
    interface(game)


if __name__ == '__main__':
    main()
