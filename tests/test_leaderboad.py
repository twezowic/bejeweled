from Bejeweled.leaderboard import Score, Leadeboard


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


def test_adding_new_score():
    leaderboard = Leadeboard()
    game_mode = 'endless'
    score1 = Score('ana', 100)
    leaderboard.adding_new_score(score1, game_mode)
    assert leaderboard.scores(game_mode) == [score1]


def test_highscore():
    leaderboard = Leadeboard()
    game_mode = 'endless'
    assert leaderboard.highscore(game_mode) == 0
