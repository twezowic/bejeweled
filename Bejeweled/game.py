from bejeweled.board import Board
from bejeweled.leaderboard import Leadeboard, Score


class Level:
    def __init__(
            self,
            goal: int,
            moves: int):
        """
        Creates instance of Level class.

        Args:
            goal (int): basic goal to achieve
            moves (int): number of moves per level
        """
        self._mode = 'normal'
        self._level = 1
        self._goal = goal
        self._moves = moves

    def mode(self) -> str:
        """
        Returns:
            str: normal or endless
        """
        return self._mode

    def change_mode(self):
        """
        Changes mode attribute is normal or endless.
        If it is normal it changes it to endless.
        And if it is endless it changes it to normal.
        """
        if self.mode() == 'normal':
            self._mode = 'endless'
        else:
            self._mode = 'normal'

    def is_normal(self) -> bool:
        """
        Returns:
            bool: is mode is normal
        """
        return self.mode() == 'normal'

    def level(self) -> int:
        """
        Returns:
            int: current level of game
        """
        return self._level

    def add_level(self):
        """
        Adds one to level counter.
        """
        self._level += 1

    def goal(self) -> int:
        """
        Returns:
            int: current goal of game.
        """
        return self._goal

    def add_goal(self):
        """
        Adds two hundred to goal to achieve.
        """
        self._goal += 200

    def moves(self) -> int:
        """
        Returns:
            int: number of moves left
        """
        return self._moves

    def one_move(self):
        """
        Substract one from moves.
        """
        self._moves -= 1

    def reset_moves(self, basic_moves: int):
        """
        Resets number of moves.

        Args:
            basic_moves (int): move to which moves attribute will be set
        """
        self._moves = basic_moves

    def win_condition(self, score: int) -> bool:
        """
        Checks if the game is in win state.

        Args:
            score (int): player's score

        Returns:
            bool: is player's score equal or greater than goal
        """
        if not self.is_normal():
            return False
        return score >= self.goal()


def is_adjacent(first_position: list, second_position: list) -> bool:
    """
    Returns is two positions are adjacent.

    Args:
        first_position (list): first position of jewel
        second_position (list): second position of jewel

    Returns:
        bool: is positions are adjacent
    """
    x1, y1 = first_position
    x2, y2 = second_position
    if (x2 - 1 == x1 or x2 + 1 == x1) and y1 == y2:
        return True
    if (y2 - 1 == y1 or y2 + 1 == y1) and x1 == x2:
        return True
    return False


class Game:
    def __init__(self, args):
        """
        Creates instance of Game class.

        Args:
            args (argparse.Namespace): namespace object of argparse class
        """
        self._arguments = args
        self._score = Score()
        self._level = Level(args.goal, args.move)
        self._board = Board(args.width, args.height, args.jewel)
        self._leaderboard = Leadeboard()

    def arguments(self):
        """
        Returns:
            arparse.Namespace: namespace object of argparse class
        """
        return self._arguments

    def score(self) -> int:
        """
        Returns:
            int: object of Score class
        """
        return self._score

    def set_score(self, new_score):
        """
        Sets score attribute.

        Args:
            new_score (Score): Score class to which it will be set
        """
        self._score = new_score

    def level(self):
        """
        Returns:
            Level: object of Level class
        """
        return self._level

    def reset_level(self):
        """
        Resets level's goal and moves.
        """
        self._level = Level(self.arguments().goal, self.arguments().move)

    def board(self):
        """
        Returns:
            Board: object of Board class
        """
        return self._board

    def set_board(self, new_board):
        """
        Sets board attribute.
        Used only testing.

        Args:
            new_board (Board): Board class to which it will be set
        """
        self._board = new_board

    def leaderboard(self):
        """
        Returns:
            Leaderboard: object of Leaderboard class
        """
        return self._leaderboard

    def next_level(self):
        """
        Prepare the game for the next level.
        """
        self.level().add_level()
        self.level().add_goal()
        self.level().reset_moves(self.arguments().move)
        self.setup_board()
        self.score().reset_score()

    def reset(self):
        """
        Reset board, score and level attributes.
        """
        self.setup_board()
        self.score().reset()
        self.reset_level()

    def moving_jewels(self, position1: list, position2: list) -> bool:
        """
        Swaps the jewels and then:
        If after the move there are at least three jewels
            in any line it returns True.

        Otherwise it swaps the jewels again and returns False.

        Args:
            position1 (list): first jewel position
            position2 (list): second jewel position

        Returns:
            bool: is valid move
        """

        if is_adjacent(position1, position2):
            self.board().swap_jewels(
                position1,
                position2
                )
            if not self.board().destroying_move():
                self.board().swap_jewels(
                    position1,
                    position2
                    )
                return False
            elif self.level().is_normal():
                self.level().one_move()
            return True
        return False

    def _is_match(self, counter: int, scored: bool) -> bool:
        """
        Returns if there are at least three in counter.
        If scored is True it adds points to player's score.

        Args:
            counter (int): number of jewels in a line
            scored (bool): is score being added

        Returns:
            bool: is at least three in a line
        """
        if counter >= 3:
            if scored:
                self.score().add_score(((2 ** (counter - 2)) * 50))
            return True
        return False

    def destroying_jewels(self, scored: bool):
        """
        Checks is there are at least three jewels in rows and columns.
        If there are it swaps them to blank.

        Args:
            scored (bool): is score being added
        """
        if not self.board().is_blank():
            board = self.board().board()
            for y in range(self.board().height()):
                first = 0
                counter = 1
                for x in range(1, self.board().width()):
                    if board[y][x] == board[y][x-1]:
                        counter += 1
                    else:
                        if self._is_match(counter, scored):
                            for i in range(first, x):
                                board[y][i].set_delete(True)
                        first = x
                        counter = 1
                if self._is_match(counter, scored):
                    for i in range(first, self.board().width()):
                        board[y][i].set_delete(True)

            for x in range(self.board().width()):
                first = 0
                counter = 1
                for y in range(1, self.board().height()):
                    if board[y][x] == board[y-1][x]:
                        counter += 1
                    else:
                        if self._is_match(counter, scored):
                            for i in range(first, y):
                                board[i][x].set_delete(True)
                        first = y
                        counter = 1
                if self._is_match(counter, scored):
                    for i in range(first, self.board().height()):
                        board[i][x].set_delete(True)

            for y in range(self.board().height()):
                for x in range(self.board().width()):
                    if board[y][x].delete():
                        board[y][x].set_colour('white')
                        board[y][x].set_delete(False)

    def setup_board(self):
        """
        Setup board so that it will be not having matches at the start
            and there is at least one possible move.
        """
        self.board().create_board()
        while self.board().game_over():
            self.board().create_board()
        while self.board().destroying_move():
            self.destroying_jewels(False)
            while self.board().is_blank():
                self.board().falling_jewels()
                self.board().new_jewels()
