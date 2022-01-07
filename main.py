from interface import interface
from board import Board
from game import Game
from leaderboard import Leadeboard


def main():
    board = Board()
    game = Game()
    leaderboard = Leadeboard()
    leaderboard.load()
    game.set_highscore(leaderboard.get_highscore())
    board.setup_board()
    interface(board, game, leaderboard)


if __name__ == '__main__':
    main()
