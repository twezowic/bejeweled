from board import Board
from config import number_of_moves, basic_goal
from leaderboard import Leadeboard, Score


class Level:
    def __init__(
            self,
            mode=None,
            which_level=1,
            goal=basic_goal,
            moves=number_of_moves):
        if mode is None:
            mode = 'normal'
        self._mode = mode
        self._level = which_level
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

    def set_goal(self):
        self._goal = (self.level() - 1) * 200 + 800

    def moves(self):
        return self._moves

    def reset_moves(self):
        self._moves = number_of_moves

    def one_move(self):
        self._moves -= 1

    def win_condition(self, score):
        if not self.is_normal():
            return False
        return score >= self.goal()


class Game:
    def __init__(
            self,
            score=Score(),
            level=Level(),
            board=Board(),
            leaderboard=Leadeboard()):
        self._score = score
        self._level = level
        self._board = board
        self._leaderboard = leaderboard

    def level(self):
        return self._level

    def reset_level(self):
        self._level = Level()

    def score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def board(self):
        return self._board

    def leaderboard(self):
        return self._leaderboard

    def next_level(self):
        self.level().add_level()
        self.level().set_goal()
        self.level().reset_moves()
        self.board().setup_board()
        self.score().reset_score()

    def reset(self):
        self.board().setup_board()
        self.score().reset()
        self.reset_level()

    def moving_jewels(self, position1, position2):
        def adjacent(first_position, second_position):
            x1, y1 = first_position
            x2, y2 = second_position
            if (x2 - 1 == x1 or x2 + 1 == x1) and y1 == y2:
                return True
            if (y2 - 1 == y1 or y2 + 1 == y1) and x1 == x2:
                return True
            return False

        if adjacent(position1, position2):
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
