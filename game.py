from config import number_of_moves
import json


def get_highscore():
    try:
        with open('highscore.txt', 'r') as file_handle:
            return int(file_handle.readline())
    except FileNotFoundError:
        return 0


def new_highscore(highscore):
    with open('highscore.txt', 'w') as file_handle:
        file_handle.writelines(f'{highscore}')


class Score:
    def __init__(self, name, score):
        self._name = name
        self._score = score

    def name(self):
        return self._name

    def score(self):
        return self._score


class Leadeboard:
    def __init__(self, scores):
        self._scores = scores

    def scores(self):
        return self._scores

    def set_scores(self, new_scores):
        self._scores = new_scores

    def get_from_json(self):
        with open('leaderboard.json', 'r') as file_handle:
            leadeboard = []
            data = json.load(file_handle)
            for element in data:
                name = element['name']
                score = element['score']
                leadeboard.append(Score(name, score))
        return Leadeboard(leadeboard)

    def set_to_json(self):
        with open('leaderboard.json', 'w') as file_handle:
            data = []
            for element in self.scores():
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
        new_leaderboard = []
        for data in leadeboard:
            if new_score.score() > data.score():
                new_leaderboard.append(new_score)
            new_leaderboard.append(data)
        self.set_scores(new_leaderboard[0:9])


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
