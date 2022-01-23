import json


class Score:
    def __init__(self, name: str = None, score: int = 0):
        """
        Creates instance of Score class.

        Args:
            name (str, optional): player's name.
            Defaults to ''.

            score (int, optional): player's score.
            Defaults to 0.
        """
        if name is None:
            name = ''
        self._name = name
        self._score = score

    def name(self) -> str:
        """
        Returns:
            str: player's name
        """
        return self._name

    def add_letter(self, letter: str):
        """
        Adds letter to the player name.
        The character must be in alphabet.
        Name cannot be longer than 10 characters.

        Args:
            letter (str): letter to be added
        """
        if letter.isalpha() and len(self.name()) < 10:
            self._name += letter

    def delete_letter(self):
        """
        Deletes last letter of player's name.
        """
        self._name = self.name()[:-1]

    def reset_name(self):
        """
        Resets player's name to ''.
        """
        self._name = ''

    def score(self) -> int:
        """
        Returns:
            int: player's score
        """
        return self._score

    def add_score(self, score: int):
        """
        Adds score to the player's score.

        Args:
            score (int): score to be added
        """
        self._score += score

    def set_score(self, new_score: int):
        """
        Sets player's score.

        Args:
            new_score (int): player's score to be set
        """
        self._score = new_score

    def reset_score(self):
        """
        Resets player's score to 0.
        """
        self._score = 0

    def reset(self):
        """
        Resets both player's name and player's score.
        """
        self.reset_name()
        self.reset_score()

    def __str__(self) -> str:
        """
        Returns:
            str: printable string representation of Score class
        """
        return f'{self.name()} {self.score()}'

    def __eq__(self, other) -> bool:
        """
        Returns True if both Scores have the same player's name and score.

        Args:
            other (Score): other instance of Score class

        Returns:
            bool: result of the comparison of Scores
        """
        cond1 = self.name() == other.name()
        cond2 = self.score() == other.score()
        return cond1 and cond2


class Leadeboard:
    def __init__(self, endless=None, normal=None):
        """
        Creates instance of Leaderboard class.

        Args:
            endless (list, optional): list with leaderboard of endless mode.
            Defaults to [].

            normal (list, optional): list with leaderboard of normal mode.
            Defaults to [].
        """
        if endless is None:
            endless = []
        self._endless = endless
        if normal is None:
            normal = []
        self._normal = normal

    def scores(self, game_mode: str) -> list:
        """
        Returns list with leaderboard of selected mode.

        Args:
            game_mode (str): endless or normal

        Returns:
            list: the best scores of selected mode.
        """
        return getattr(self, '_'+game_mode)

    def set_scores(self, game_mode: str, scores: list):
        """
        Sets selected mode leaderboard with new list of scores.

        Args:
            game_mode (str): endless or normal

            scores (list): list of new leaderboard
        """
        setattr(self, '_'+game_mode, scores)

    def load(self, file):
        """
        Loads both modes leaderboard from selected file.
        Sets them to scores attributes.

        Args:
            file (file object):
            json file from which leaderboard should be loaded
        """
        data = json.load(file)
        leaderboard_normal = []
        leaderboard_endless = []
        for mode in ['normal', 'endless']:
            leaderboard = data[0][mode]
            for element in leaderboard:
                name = element['name']
                score = element['score']
                eval(f'leaderboard_{mode}').append(Score(name, score))
        self.set_scores('normal', leaderboard_normal)
        self.set_scores('endless', leaderboard_endless)

    def load_from_file(self):
        """
        Tries to open file with path Bejeweled/leaderboard.json.
        Performs load method if file exist.
        Otherswise sets both scores with empty list.
        """
        try:
            with open('Bejeweled/leaderboard.json', 'r') as file:
                self.load(file)
        except FileNotFoundError:
            self.set_scores('normal', [])
            self.set_scores('endless', [])

    def save(self, file):
        """
        Saves both modes leaderboard to selected file.

        Args:
            file (file object):
            json file to which leaderboard should be saved
        """
        data = []
        normal = []
        endless = []
        for element in self.scores('normal'):
            name = element.name()
            score = element.score()
            score_data = {
                'name': name,
                'score': score
            }
            normal.append(score_data)

        for element in self.scores('endless'):
            name = element.name()
            score = element.score()
            score_data = {
                'name': name,
                'score': score
            }
            endless.append(score_data)

        mode = {
            'normal': normal,
            'endless': endless
        }

        data.append(mode)
        json.dump(data, file, indent=4)

    def save_to_file(self):
        """
        Opens file with path 'Bejeweled/leaderboard.json'.
        Performs save method.
        """
        with open('Bejeweled/leaderboard.json', 'w') as file:
            self.save(file)

    def __str__(self, game_mode: str) -> str:
        """
        Returns printable string representation of Leaderboard class.

        Args:
            game_mode (str): endless or normal

        Returns:
            str: Leaderboard string representation
        """
        scores = self.scores(game_mode)
        result = ''
        for index, score in enumerate(scores):
            result += f'{index}. Player: {score.name()} {score.score()}\n'
        return result

    def adding_new_score(self, new_score, game_mode: str):
        """
        Adds score to selected leaderboard mode.
        Sorts all of scores and saves the best ten them.

        Args:
            new_score (Score): score to be added

            game_mode (str): endless or normal
        """
        leadeboard = self.scores(game_mode)
        leadeboard.append(new_score)
        leadeboard.sort(key=lambda score: score.score(), reverse=True)
        self.set_scores(game_mode, leadeboard[:10])

    def highscore(self, game_mode: str) -> int:
        """
        Returns the highscore of selected mode.
        If the selected leaderboard is empty returns 0.

        Args:
            game_mode (str): endless or normal

        Returns:
            int: the best score
        """
        if not self.scores(game_mode):
            return 0
        return self.scores(game_mode)[0].score()
