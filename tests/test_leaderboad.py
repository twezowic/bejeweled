from Bejeweled.leaderboard import Score, Leadeboard
from io import StringIO


def test_add_letter():
    score = Score()
    score.add_letter('a')
    assert score.name() == 'a'
    score.add_letter('P')
    assert score.name() == 'aP'


def test_add_letter_not_alphabet():
    score = Score()
    score.add_letter('1')
    assert score.name() == ''
    score.add_letter('$')
    assert score.name() == ''


def test_add_letter_more_than_10_characters():
    score = Score()
    for i in range(10):
        score.add_letter('a')
    assert score.name() == 'a' * 10
    score.add_letter('b')
    assert score.name() == 'a' * 10


def test_delete_letter():
    score = Score()
    score.add_letter('a')
    assert score.name() == 'a'
    score.add_letter('b')
    assert score.name() == 'ab'
    score.delete_letter()
    assert score.name() == 'a'


def test_reset_name():
    score = Score()
    for i in range(10):
        score.add_letter('b')
    assert score.name() == 'b' * 10
    score.reset_name()
    assert score.name() == ''


def test_add_score():
    score = Score()
    score.add_score(100)
    assert score.score() == 100


def test_reset_score():
    score = Score()
    score.add_score(100)
    assert score.score() == 100
    score.reset_score()
    assert score.score() == 0


def test_reset_both():
    score = Score()
    score.add_score(100)
    assert score.score() == 100
    score.add_letter('a')
    assert score.name() == 'a'
    score.reset()
    assert score.name() == ''
    assert score.score() == 0


def test_equals():
    score1 = Score('ana', 1000)
    score2 = Score('ana', 1000)
    score3 = Score('bob', 1000)
    score4 = Score('ana', 1100)
    assert score1 == score2
    assert score1 != score3
    assert score1 != score4


def test_set_scores():
    leaderboard = Leadeboard()
    score1 = Score('ana', 1000)
    leaderboard.set_scores('endless', [score1])
    assert leaderboard.scores('endless') == [score1]
    score2 = Score('bob', 1000)
    leaderboard.set_scores('normal', [score2])
    assert leaderboard.scores('normal') == [score2]


def test_load():
    leaderboard = Leadeboard()
    file = StringIO('''
    [
    {
        "name": "john",
        "score": 400
    },
    {
        "name": "bob",
        "score": 300
    }
    ]
    ''')
    leaderboard.load('endless', file)
    assert leaderboard.scores('endless') == [
        Score('john', 400),
        Score('bob', 300)
        ]


def test_save():
    leaderboard = Leadeboard([
        Score('john', 400),
        Score('bob', 300)
        ])
    file = StringIO()
    leaderboard.save('endless', file)
    file.seek(0)
    assert file.read() == '''[
    {
        "name": "john",
        "score": 400
    },
    {
        "name": "bob",
        "score": 300
    }
]'''
    # print(file.read())


def test_adding_new_score():
    leaderboard = Leadeboard()
    game_mode = 'endless'
    score1 = Score('ana', 100)
    leaderboard.adding_new_score(score1, game_mode)
    assert leaderboard.scores(game_mode) == [score1]


def test_adding_new_score_more_than_10():
    leaderboard = Leadeboard(
        [
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100)
        ],
        [
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100)
        ]
    )
    leaderboard.adding_new_score(Score('b', 100), 'endless')
    assert leaderboard.scores('endless') == [
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100)
        ]
    leaderboard.adding_new_score(Score('b', 1000), 'normal')
    assert leaderboard.scores('normal') == [
            Score('b', 1000),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100),
            Score('a', 100)
        ]


def test_highscore():
    leaderboard = Leadeboard()
    game_mode = 'endless'
    assert leaderboard.highscore(game_mode) == 0
