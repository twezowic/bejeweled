from board import Board
from config import number_of_moves, basic_goal
from leaderboard import Leadeboard, Score


class Level:
    def __init__(
            self,
            normal=True,
            which_level=1,
            goal=basic_goal,
            moves=number_of_moves):
        self._normal = normal
        self._level = which_level
        self._goal = goal
        self._moves = moves

    def normal(self):
        return self._normal

    def change_normal(self):
        self._normal = not self.normal()

    def level(self):
        return self._level

    def next_level(self, game):
        self._level += 1
        self.set_goal()
        self.reset_moves()
        game.reset()

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
        if not self.normal():
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
        leaderboard.load('endless')
        leaderboard.load('normal')
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

    def reset(self):
        self.board().setup_board()
        self.score().reset_score()
        self.reset_level()
