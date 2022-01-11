import json


class Score:
    def __init__(self, name=None, score=0):
        if name is None:
            name = ''
        self._name = name
        self._score = score

    def name(self):
        return self._name

    def add_letter(self, letter):
        if len(self.name()) < 10:
            self._name = self.name() + letter

    def delete_letter(self):
        self._name = self.name()[:-1]

    def reset_name(self):
        self._name = ''

    def score(self):
        return self._score

    def add_score(self, score_to_add):
        self._score = self.score() + score_to_add

    def reset_score(self):
        self._score = 0

    def __str__(self) -> str:
        return f'{self.name():<10} {self.score():>10}'

    def __eq__(self, other) -> bool:
        cond1 = self.name() == other.name()
        cond2 = self.score() == other.score()
        return cond1 and cond2


class Leadeboard:
    def __init__(self, endless=None, normal=None):
        if endless is None:
            endless = []
        self._endless = endless
        if normal is None:
            normal = []
        self._normal = normal

    def scores(self, game_mode):
        return getattr(self, '_'+game_mode)

    def set_endless(self, new_scores):
        self._scores = new_scores

    def set_normal(self, new_normal):
        self._normal = new_normal

    def load(self, game_mode):
        try:
            with open(f'leaderboard_{game_mode}.json', 'r') as file_handle:
                leadeboard = []
                data = json.load(file_handle)
                for element in data:
                    name = element['name']
                    score = element['score']
                    leadeboard.append(Score(name, score))
            getattr(self, 'set_'+game_mode)(leadeboard)
        except FileNotFoundError:
            return []

    def save(self, game_mode):
        with open(f'leaderboard_{game_mode}.json', 'w') as file_handle:
            data = []
            leadeboard = self.scores(game_mode)
            for element in leadeboard:
                name = element.name()
                score = element.score()
                score_data = {
                    'name': name,
                    'score': score
                }
                data.append(score_data)
            json.dump(data, file_handle, indent=4)

    def __str__(self, game_mode):
        scores = self.scores(game_mode)
        result = ''
        for index, score in enumerate(scores):
            result += f'{index}. Player: {score.name()} {score.score()}\n'
        return result

    def adding_new_score(self, new_score, game_mode):
        leadeboard = self.scores(game_mode)
        setter = getattr(self, 'set_'+game_mode)
        if not leadeboard:
            setter([new_score])
            print(leadeboard)
        else:
            leadeboard.append(new_score)
            leadeboard.sort(key=lambda score: score.score(), reverse=True)
            if len(leadeboard) > 10:
                setter(leadeboard[:10])

    def highscore(self, game_mode):
        if not self.scores(game_mode):
            return 0
        return getattr(self, game_mode)()[0].score()
