from config import number_of_moves


class Game:
    def __init__(self, score=0, moves=number_of_moves, normal_mode=True, name=None, highscore=0):
        self._moves = moves
        self._score = score
        self._normal_mode = normal_mode
        if name is None:
            name = ''
        self._name = name
        self._highscore = highscore

    def moves(self):
        return self._moves

    def set_moves(self, new_moves):
        self._moves = new_moves

    def one_move(self):
        self.set_moves(self.moves()-1)

    def score(self):
        return self._score

    def set_score(self, new_score):
        self._score = new_score

    def normal_mode(self):
        return self._normal_mode

    def change_normal_mode(self):
        self._normal_mode = not self.normal_mode()

    def name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def highscore(self):
        return self._highscore

    def set_highscore(self, new_highscore):
        self._highscore = new_highscore
