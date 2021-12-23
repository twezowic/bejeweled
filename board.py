from config import board_width, board_height, colors_of_jewels
from numpy import array
from random import choice


class Board:
    def __init__(self, board=None):
        if board is None:
            board = []
        self._board = board

    def board(self):
        return self._board

    def set_board(self, new_board):
        self._board = new_board

    def create_board(self):  # x, y; ma generować tablicę bez usuwań
        board = []
        for row in range(board_width):
            line = []
            for jewel in range(board_height):
                jewel = choice(colors_of_jewels)
                line.append(jewel)
            board.append(line)
        board = array(board)
        self.set_board(board)

    def destroy_jewels(self):
        pass
