import interface
from board import Board
from game import Player


def main():
    board = Board()
    player = Player()
    board.create_board()
    board.show_board()
    interface.interface(board, player)


if __name__ == '__main__':
    main()
