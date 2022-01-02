from config import number_of_moves
import json


class Score:
    def __init__(self, name, score):
        self._name = name
        self._score = score

    def name(self):
        return self._name

    def score(self):
        return self._score


class Leadeboard:
    def __init__(self, scores=None):
        if scores is None:
            scores = []
        self._scores = scores

    def scores(self):
        return self._scores

    def set_scores(self, new_scores):
        self._scores = new_scores

    def get_from_json(self):
        try:
            with open('leaderboard.json', 'r') as file_handle:
                leadeboard = []
                data = json.load(file_handle)
                for element in data:
                    name = element['name']
                    score = element['score']
                    leadeboard.append(Score(name, score))
            self.set_scores(leadeboard)
        except FileNotFoundError:
            return None

    def set_to_json(self):
        with open('leaderboard.json', 'w') as file_handle:
            data = []
            leadeboard = self.scores()
            for element in leadeboard:
                name = element.name()
                score = element.score()
                score_data = {
                    'name': name,
                    'score': score
                }
                data.append(score_data)
            json.dump(data, file_handle, indent=4)

    def __str__(self):
        scores = self.scores()
        result = ''
        for index, score in enumerate(scores):
            result += f'{index}. Player: {score.name()} {score.score()}\n'
        return result

    def adding_new_score(self, new_score):
        leadeboard = self.scores()
        if not leadeboard:
            self.set_scores([new_score])
        else:
            leadeboard.append(new_score)
            leadeboard.sort(key=lambda score: score.score(), reverse=True)
            if len(leadeboard) > 10:
                self.set_scores(leadeboard[:9])

    def get_highscore(self):
        if not self.scores():
            return 0
        return self.scores()[0].score()


class Game:
    def __init__(self, score=0, moves=number_of_moves):
        self._moves = moves
        self._score = score

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
