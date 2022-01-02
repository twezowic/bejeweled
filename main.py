from interface import interface
from board import Board
from game import Game, Leadeboard


def main():
    board = Board()
    game = Game()
    leaderboard = Leadeboard()
    leaderboard.get_from_json()
    board.create_board()
    board.setup_board()
    interface(board, game, leaderboard)


if __name__ == '__main__':
    main()
