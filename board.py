from config import board_width, board_height, colors_of_jewels
from numpy import array
from random import choice


class Jewel:
    def __init__(self, colour):
        self._colour = colour

    def colour(self):
        return self._colour


class Board:
    def __init__(self, board=None):
        if board is None:
            board = []
        self._board = board

    def board(self):
        return self._board

    def set_board(self, new_board):
        self._board = new_board

    def create_board(self):
        board = []
        for x in range(board_height):
            line = []
            for y in range(board_width):
                jewel = Jewel(choice(colors_of_jewels))
                line.append(jewel)
            board.append(line)
        board = array(board)
        self.set_board(board)

    def destroy_jewels(self):
        pass

    def show_board(self):
        table = self.board()
        for i in range(board_height):
            for j in range(board_width):
                print(table[i][j].colour())

    def swap_jewels(self, position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        table = self.board()
        table[x1][y1], table[x2][y2] = table[x2][y2], table[x1][y1]
