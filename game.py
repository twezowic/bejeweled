from config import number_of_moves
from leaderboard import Score


class Game:
    def __init__(
            self,
            score=Score(),
            moves=number_of_moves,
            normal_mode=True,
            highscore=0):
        self._moves = moves
        self._score = score
        self._normal_mode = normal_mode
        self._highscore = highscore

    def moves(self):
        return self._moves

    def set_moves(self, new_moves):
        self._moves = new_moves

    def one_move(self):
        self.set_moves(self.moves()-1)

    def score(self):
        return self._score

    def normal_mode(self):
        return self._normal_mode

    def change_normal_mode(self):
        self._normal_mode = not self.normal_mode()

    def highscore(self):
        return self._highscore

    def set_highscore(self, new_highscore):
        self._highscore = new_highscore

    def reset(self, board):
        board.setup_board(self)
        self.set_moves(number_of_moves)
        self._score = Score()
        self._normal_mode = True


class Level:
    def __init__(self) -> None:
        pass
