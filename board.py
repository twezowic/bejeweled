from config import board_width, board_height, colors_of_jewels
from numpy import array
from random import choice


class Jewel:
    def __init__(self, colour, special=False):
        self._colour = colour
        self._special = special

    def colour(self):
        return self._colour

    def special(self):
        return self._special


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
        for y in range(board_height):
            line = []
            for x in range(board_width):
                jewel = Jewel(choice(colors_of_jewels))
                line.append(jewel)
            board.append(line)
        board = array(board)
        self.set_board(board)

    def destroy_jewels(self):
        pass

    def show_board(self):
        table = self.board()
        for y in range(board_height):
            line = ''
            for x in range(board_width):
                line += f'{table[y][x].colour()}'
            print(line)

    def swap_jewels(self, position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        table = self.board()
        table[y1][x1], table[y2][x2] = table[y2][x2], table[y1][x1]
