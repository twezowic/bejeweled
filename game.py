from config import number_of_moves


def get_highscore():
    try:
        with open('highscore.txt', 'r') as file_handle:
            return int(file_handle.readline())
    except FileNotFoundError:
        return 0


def new_highscore(highscore):
    with open('highscore.txt', 'w') as file_handle:
        file_handle.writelines(f'{highscore}')


class Player:
    def __init__(self, moves=number_of_moves):
        self._moves = moves

    def moves(self):
        return self._moves

    def set_moves(self, new_moves):
        self._moves = new_moves

    def one_move(self):
        self.set_moves(self.moves()-1)
