from interface import interface
from board import Board
from game import Player


def main():
    board = Board()
    player = Player()
    board.create_board()
    board.setup_board()
    interface(board, player)


if __name__ == '__main__':
    main()
