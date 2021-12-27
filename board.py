from config import board_width, board_height, colors_of_jewels
from random import choice
from numpy import array


class Jewel:
    def __init__(self, colour, delete=False):
        self._colour = colour
        self._delete = delete

    def colour(self):
        return self._colour

    def delete(self):
        return self._delete

    def set_delete(self, new_delete):
        self._delete = new_delete

    def set_colour(self, new_colour):
        self._colour = new_colour

    def __eq__(self, other) -> bool:
        return self.colour() == other.colour()

    def __str__(self) -> str:
        return f'{self.colour()}'


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

    def destroying_jewels(self):
        board = self.board()
        for y in range(board_height):  # wiersze
            for x in range(board_width - 2):
                three = board[y, x:x+3]
                if three[0] == three[1] == three[2]:
                    for element in range(3):
                        board[y][x+element].set_delete(True)
        for x in range(board_width):  # kolumny
            for y in range(board_height - 2):
                three = board[y:y+3, x]
                if three[0] == three[1] == three[2]:
                    for element in range(3):
                        board[y+element][x].set_delete(True)
        for y in range(board_height):  # usuwanie
            for x in range(board_width):
                if board[y][x].delete():
                    board[y][x].set_colour('white')
                    board[y][x].set_delete(False)
