from bejeweled.board import Board
from bejeweled.leaderboard import Leadeboard, Score


class Level:
    def __init__(
            self,
            goal,
            moves,):
        self._mode = 'normal'
        self._level = 1
        self._goal = goal
        self._moves = moves

    def mode(self):
        return self._mode

    def change_mode(self):
        if self.mode() == 'normal':
            self._mode = 'endless'
        else:
            self._mode = 'normal'

    def is_normal(self):
        return self.mode() == 'normal'

    def level(self):
        return self._level

    def add_level(self):
        self._level += 1

    def goal(self):
        return self._goal

    def add_goal(self):
        self._goal += 200

    def moves(self):
        return self._moves

    def one_move(self):
        self._moves -= 1

    def reset_moves(self, basic_moves):
        self._moves = basic_moves

    def win_condition(self, score):
        if not self.is_normal():
            return False
        return score >= self.goal()


def is_adjacent(first_position, second_position):
    x1, y1 = first_position
    x2, y2 = second_position
    if (x2 - 1 == x1 or x2 + 1 == x1) and y1 == y2:
        return True
    if (y2 - 1 == y1 or y2 + 1 == y1) and x1 == x2:
        return True
    return False


class Game:
    def __init__(self, args):
        self._arguments = args
        self._score = Score()
        self._level = Level(args.goal, args.move)
        self._board = Board(args.width, args.height, args.jewel)
        self._leaderboard = Leadeboard()

    def arguments(self):
        return self._arguments

    def score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def level(self):
        return self._level

    def reset_level(self):
        self._level = Level(self.arguments().goal, self.arguments().move)

    def board(self):
        return self._board

    def set_board(self, new_board):
        self._board = new_board

    def leaderboard(self):
        return self._leaderboard

    def next_level(self):
        self.level().add_level()
        self.level().add_goal()
        self.level().reset_moves(self.arguments().move)
        self.setup_board()
        self.score().reset_score()

    def reset(self):
        self.setup_board()
        self.score().reset()
        self.reset_level()

    def moving_jewels(self, position1, position2):
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

    def _is_match(self, counter, scored):
        if counter >= 3:
            if scored:
                self.score().add_score(((2 ** (counter - 2)) * 50))
            return True
        return False

    def destroying_jewels(self, scored):
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

            for y in range(self.board().height()):  # usuwanie
                for x in range(self.board().width()):
                    if board[y][x].delete():
                        board[y][x].set_colour('white')
                        board[y][x].set_delete(False)
            self.board().set_board(board)

    def setup_board(self):
        self.board().create_board()
        while self.board().game_over():
            self.board().create_board()
        while self.board().destroying_move():
            self.destroying_jewels(False)
            while self.board().is_blank():
                self.board().falling_jewels()
                self.board().new_jewels()
