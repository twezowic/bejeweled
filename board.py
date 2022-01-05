from config import board_width, board_height, colors_of_jewels
from random import choice
from numpy import array
from time import sleep


class Jewel:
    def __init__(self, colour, delete=False):
        self._colour = colour
        self._delete = delete

    def colour(self):
        return self._colour

    def set_colour(self, new_colour):
        self._colour = new_colour

    def delete(self):
        return self._delete

    def set_delete(self, new_delete):
        self._delete = new_delete

    def __eq__(self, other) -> bool:
        return self.colour() == other.colour()


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

    def destroying_move(self):
        board = self.board()
        for y in range(board_height):  # wiersze
            for x in range(board_width - 2):
                three = board[y, x:x+3]
                if three[0] == three[1] == three[2]:
                    return True
        for x in range(board_width):  # kolumny
            for y in range(board_height - 2):
                three = board[y:y+3, x]
                if three[0] == three[1] == three[2]:
                    return True
        return False

    def setup_board(self):
        while self.destroying_move():
            self.destroying_jewels()
            while self.is_blank():
                self.falling_jewels()
                self.new_jewels()

    def swap_jewels(self, position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        table = self.board()
        table[y1][x1], table[y2][x2] = table[y2][x2], table[y1][x1]

    def destroying_jewels(self):
        score = 0
        if not self.is_blank():
            board = self.board()
            for y in range(board_height):  # wiersze
                for x in range(board_width - 2):
                    three = board[y, x:x+3]
                    if three[0] == three[1] == three[2] and three[0].colour() != 'white':
                        for element in range(3):
                            board[y][x+element].set_delete(True)
            for x in range(board_width):  # kolumny
                for y in range(board_height - 2):
                    three = board[y:y+3, x]
                    if three[0] == three[1] == three[2] and three[0].colour() != 'white':
                        for element in range(3):
                            board[y+element][x].set_delete(True)
            for y in range(board_height):  # usuwanie
                for x in range(board_width):
                    if board[y][x].delete():
                        score += 100
                        board[y][x].set_colour('white')
                        board[y][x].set_delete(False)
        return score

    def falling_jewels(self):
        board = self.board()
        for y in range(board_height-1, 0, -1):
            for x in range(board_width):
                if board[y][x].colour() == 'white':
                    self.swap_jewels((x, y), (x, y - 1))

    def new_jewels(self):
        board = self.board()
        for x in range(board_width):
            if board[0][x].colour() == 'white':
                board[0][x].set_colour(choice(colors_of_jewels))

    def is_blank(self):
        board = self.board()
        for y in range(board_height):
            for x in range(board_width):
                if board[y][x].colour() == 'white':
                    return True
        return False

    def jewel_refill(self):
        if self.is_blank():
            self.falling_jewels()
            self.new_jewels()
            sleep(0.75)

    def game_over(self, number_of_moves):
        if self.is_blank():
            return False
        if number_of_moves == 0:
            return True
        for y in range(board_height):  # wiersze
            for x in range(board_width - 1):
                self.swap_jewels((x, y), (x+1, y))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x+1, y))
        for x in range(board_width):  # kolumny
            for y in range(board_height - 1):
                self.swap_jewels((x, y), (x, y+1))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x, y+1))
        return True
