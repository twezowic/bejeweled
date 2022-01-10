from config import number_of_moves
from leaderboard import Score


class Level:
    def __init__(
            self,
            normal_mode=True,
            which_level=1,
            goal=800,
            moves=number_of_moves):
        self._normal_mode = normal_mode
        self._level = which_level
        self._goal = goal
        self._moves = moves

    def normal_mode(self):
        return self._normal_mode

    def change_normal_mode(self):
        self._normal_mode = not self.normal_mode()

    def level(self):
        return self._level

    def next_level(self, game, board):
        self._level += 1
        self.add_to_goal(200)
        game.reset(board)

    def goal(self):
        return self._goal

    def add_to_goal(self, added_goal):
        self._goal += added_goal

    def moves(self):
        return self._moves

    def set_moves(self, new_moves):
        self._moves = new_moves

    def one_move(self):
        self.set_moves(self.moves()-1)

    def win_condition(self, score):
        if not self.normal_mode():
            return False
        return score >= self.goal()


class Game:
    def __init__(
            self,
            score=Score(),
            level=Level(),
            highscore=0):
        self._score = score
        self._level = level
        self._highscore = highscore

    def level(self):
        return self._level

    def score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def highscore(self):
        return self._highscore

    def set_highscore(self, new_highscore):
        self._highscore = new_highscore

    def reset(self, board):
        board.setup_board()
        self.set_score(Score())
