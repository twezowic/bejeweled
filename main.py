import interface
from board import Board


def main():
    board = Board()
    board.create_board()
    interface.interface(board)


if __name__ == '__main__':
    main()
