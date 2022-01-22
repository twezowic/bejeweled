from random import choice
from colorsys import hls_to_rgb


def _choose_colors(number_of_colors):
    colors = []
    for i in range(1, number_of_colors+1):
        h, l, s = (i/number_of_colors, 0.5, 1.0)
        r, g, b = [int(255*i) for i in hls_to_rgb(h, l, s)]
        colors.append((r, g, b))
    return colors


class Jewel:
    def __init__(self, colour):
        self._colour = colour
        self._delete = False

    def colour(self):
        return self._colour

    def set_colour(self, new_colour):
        self._colour = new_colour

    def delete(self):
        return self._delete

    def set_delete(self, new_delete):
        self._delete = new_delete

    def __eq__(self, other) -> bool:
        if self.colour() == 'white':
            return False
        return self.colour() == other.colour()


class Board:
    def __init__(self, width, height, num_col, board=None):
        self._width = width
        self._height = height
        self._colors = _choose_colors(num_col)
        if board is None:
            board = []
        self._board = board

    def width(self):
        return self._width

    def height(self):
        return self._height

    def colors(self):
        return self._colors

    def board(self):
        return self._board

    def set_board(self, new_board):
        self._board = new_board

    def create_board(self):
        board = []
        for y in range(self.height()):
            line = []
            for x in range(self.width()):
                jewel = Jewel(choice(self.colors()))
                line.append(jewel)
            board.append(line)
        self.set_board(board)

    def show_board(self):
        board = self.board()
        for y in range(self.height()):
            line = ''
            for x in range(self.width()):
                line += f'{board[y][x].colour()}'
            print(line)

    def destroying_move(self):
        board = self.board()
        for y in range(self.height()):  # wiersze
            counter = 1
            for x in range(1, self.width()):
                if board[y][x] == board[y][x-1]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True
        for x in range(self.width()):  # kolumny
            counter = 1
            for y in range(1, self.height()):
                if board[y][x] == board[y-1][x]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True
        return False

    def swap_jewels(self, position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        board = self.board()
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def falling_jewels(self):
        board = self.board()
        for y in range(self.height()-1, 0, -1):
            for x in range(self.width()):
                if board[y][x].colour() == 'white':
                    self.swap_jewels((x, y), (x, y - 1))

    def new_jewels(self):
        board = self.board()
        for x in range(self.width()):
            if board[0][x].colour() == 'white':
                board[0][x].set_colour(choice(self.colors()))

    def is_blank(self):
        board = self.board()
        for y in range(self.height()):
            for x in range(self.width()):
                if board[y][x].colour() == 'white':
                    return True
        return False

    def jewel_refill(self):
        self.falling_jewels()
        self.new_jewels()

    def game_over(self, normal=False, number_of_moves=1):
        if self.is_blank():
            return False
        if normal and number_of_moves == 0:
            return True
        for y in range(self.height()):  # wiersze
            for x in range(self.width() - 1):
                self.swap_jewels((x, y), (x+1, y))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x+1, y))
        for x in range(self.width()):  # kolumny
            for y in range(self.height() - 1):
                self.swap_jewels((x, y), (x, y+1))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x, y+1))
        return True
