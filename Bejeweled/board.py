from config import board_width, board_height, number_of_jewels
from random import choice
from colorsys import hls_to_rgb


def choose_colors(number_of_colors):
    colors = []
    for i in range(1, number_of_colors+1):
        h, l, s = (i/number_of_colors, 0.5, 1.0)
        r, g, b = [255*i for i in hls_to_rgb(h, l, s)]
        colors.append((r, g, b))
    return colors


colors_of_jewels = choose_colors(number_of_jewels)


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
        if self.colour == 'white':
            return False
        return self.colour() == other.colour()


def _is_match(counter, game):
    if counter >= 3:
        if game is not None:
            game.score().add_score(((2 ** (counter - 2)) * 50))
        return True
    return False


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
        self.set_board(board)

    def show_board(self):
        board = self.board()
        for y in range(board_height):
            line = ''
            for x in range(board_width):
                line += f'{board[y][x].colour()}'
            print(line)

    def destroying_move(self):
        board = self.board()
        for y in range(board_height):  # wiersze
            counter = 1
            for x in range(1, board_width):
                if board[y][x] == board[y][x-1]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True
        for x in range(board_width):  # kolumny
            counter = 1
            for y in range(1, board_height):
                if board[y][x] == board[y-1][x]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True
        return False

    def setup_board(self):
        self.create_board()
        while self.game_over():
            self.create_board()
        while self.destroying_move():
            self.destroying_jewels()
            while self.is_blank():
                self.falling_jewels()
                self.new_jewels()

    def swap_jewels(self, position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        board = self.board()
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def destroying_jewels(self, game=None):
        if not self.is_blank():
            board = self.board()
            for y in range(board_height):
                first = 0
                counter = 1
                for x in range(1, board_width):
                    if board[y][x] == board[y][x-1]:
                        counter += 1
                    else:
                        if _is_match(counter, game):
                            for i in range(first, x):
                                board[y][i].set_delete(True)
                        first = x
                        counter = 1
                if _is_match(counter, game):
                    for i in range(first, board_width):
                        board[y][i].set_delete(True)

            for x in range(board_width):
                first = 0
                counter = 1
                for y in range(1, board_height):
                    if board[y][x] == board[y-1][x]:
                        counter += 1
                    else:
                        if _is_match(counter, game):
                            for i in range(first, y):
                                board[i][x].set_delete(True)
                        first = y
                        counter = 1
                if _is_match(counter, game):
                    for i in range(first, board_height):
                        board[i][x].set_delete(True)

            for y in range(board_height):  # usuwanie
                for x in range(board_width):
                    if board[y][x].delete():
                        board[y][x].set_colour('white')
                        board[y][x].set_delete(False)

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
        self.falling_jewels()
        self.new_jewels()

    def game_over(self, number_of_moves=1, normal=False):
        if self.is_blank():
            return False
        if number_of_moves == 0 and normal:
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
