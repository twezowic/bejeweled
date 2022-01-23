from random import choice
from colorsys import hls_to_rgb


def _choose_colors(number_of_colors: int) -> list:
    """
    Creates list with evenly spaced colors.

    Args:
        number_of_colors (int): number of colors to be sellected

    Returns:
        list: chosen colors
    """

    colors = []
    for i in range(1, number_of_colors+1):
        h, l, s = (i/number_of_colors, 0.5, 1.0)
        r, g, b = [int(255*i) for i in hls_to_rgb(h, l, s)]
        colors.append((r, g, b))
    return colors


class Jewel:
    def __init__(self, colour):
        """
        Creates instance of Jewel class.

        Args:
            colour (list/str): colour of the jewel

            delete (bool) : is jewel to be swaped to blank
        """
        self._colour = colour
        self._delete = False

    def colour(self):
        """
        Returns:
            list/str: colour of the jewel
        """
        return self._colour

    def set_colour(self, new_colour):
        """
        Sets new colour of the jewel.

        Args:
            new_colour (list/str): colour to which jewel will be set
        """
        self._colour = new_colour

    def delete(self):
        """
        Returns:
            bool: is jewel to be swaped to blank
        """
        return self._delete

    def set_delete(self, new_delete):
        """
        Sets value of delete attribute.

        Args:
            new_delete (bool): value of delete to be set
        """
        self._delete = new_delete

    def __eq__(self, other) -> bool:
        """
        Returns True if both Jewels have the same colour but no white.

        Args:
            other (Jewel): other instance of Jewel class

        Returns:
            bool: result of the comparison of Jewels
        """
        if self.colour() == 'white':
            return False
        return self.colour() == other.colour()

    def is_same_colour(self, other):
        """
        Returns True if both Jewels have the same colour.
        Used only in testing.

        Args:
            other (Jewel): other instance of Jewel class

        Returns:
            bool: result of the comparison of Jewels
        """
        return self.colour() == other.colour()


class Board:
    def __init__(self, width: int, height: int, num_col: int, board=None):
        """
        Creates instance of board class.

        Args:
            width (int): board's width

            height (int): board's height

            num_col (int): number of colors of jewels

            board (list, optional): two dimentional list with jewels.
            Defaults to None.
        """
        self._width = width
        self._height = height
        self._colors = _choose_colors(num_col)
        if board is None:
            board = []
        self._board = board

    def width(self) -> int:
        """
        Returns:
            int: board's width
        """
        return self._width

    def height(self) -> int:
        """
        Returns:
            int: board's height
        """
        return self._height

    def colors(self) -> list:
        """
        Returns:
            list: list of chosen colors of jewels
        """
        return self._colors

    def board(self) -> list:
        """
        Returns:
            list: two dimentional list with jewels
        """
        return self._board

    def set_board(self, new_board: list):
        """
        Sets new board.

        Args:
            new_board (list): list to which board will be set
        """
        self._board = new_board

    def create_board(self):
        """
        Creates board with random jewels from chosen colors.
        """
        board = []
        for y in range(self.height()):
            line = []
            for x in range(self.width()):
                jewel = Jewel(choice(self.colors()))
                line.append(jewel)
            board.append(line)
        self.set_board(board)

    def __str__(self):
        """
        Returns printable string representation of Board class.
        """
        board = self.board()
        for y in range(self.height()):
            line = ''
            for x in range(self.width()):
                line += f'{board[y][x].colour()} '
            print(line)

    def destroying_move(self) -> bool:
        """
        Checks board's rows and columns
            is there are at least three jewels in a row.

        Returns:
            bool: is at least three jewels in a row.
        """
        board = self.board()
        for y in range(self.height()):
            counter = 1
            for x in range(1, self.width()):
                if board[y][x] == board[y][x-1]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True

        for x in range(self.width()):
            counter = 1
            for y in range(1, self.height()):
                if board[y][x] == board[y-1][x]:
                    counter += 1
                else:
                    counter = 1
                if counter >= 3:
                    return True
        return False

    def swap_jewels(self, position1: list, position2: list):
        """
        Swaps jewels with given positions

        Args:
            position1 (list): first jewel position

            position2 (list): second jewel position
        """
        x1, y1 = position1
        x2, y2 = position2
        board = self.board()
        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]

    def falling_jewels(self):
        """
        Make jewels fall if there are blanks jewel below it.
        """
        board = self.board()
        for y in range(self.height()-1, 0, -1):
            for x in range(self.width()):
                if board[y][x].colour() == 'white':
                    self.swap_jewels((x, y), (x, y - 1))

    def new_jewels(self):
        """
        Adds random jewels from top if there are blank jewels there.
        """
        board = self.board()
        for x in range(self.width()):
            if board[0][x].colour() == 'white':
                board[0][x].set_colour(choice(self.colors()))

    def is_blank(self) -> bool:
        """
        Checks is there are blank jewels on board.

        Returns:
            bool: is there are white colour in board
        """
        board = self.board()
        for y in range(self.height()):
            for x in range(self.width()):
                if board[y][x].colour() == 'white':
                    return True
        return False

    def jewel_refill(self):
        """
        Make jewels fall down and appear from top.
        """
        self.falling_jewels()
        self.new_jewels()

    def game_over(
            self,
            normal:
            bool = False,
            number_of_moves: int = 1) -> bool:
        """
        Checks if the game is in game over state:
            If there any blanks in board returns False.

            If normal mode and no moves left returns True.

            If there are no possible moves left returns True.

        Args:
            normal (bool, optional): is game in normal mode.
            Defaults to False.

            number_of_moves (int, optional): number of moves left in game.
            Default used only in endless mode.
            Defaults to 1.

        Returns:
            bool: is game in game over state
        """
        if self.is_blank():
            return False
        if normal and number_of_moves == 0:
            return True
        for y in range(self.height()):
            for x in range(self.width() - 1):
                self.swap_jewels((x, y), (x+1, y))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x+1, y))
        for x in range(self.width()):
            for y in range(self.height() - 1):
                self.swap_jewels((x, y), (x, y+1))
                if self.destroying_move():
                    self.swap_jewels((x, y), (x+1, y))
                    return False
                self.swap_jewels((x, y), (x, y+1))
        return True
