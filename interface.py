import pygame
from sys import exit
from config import (
    board_height,
    board_width,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
    )


def adjacent(first_position, second_position):
    x1, y1 = first_position
    x2, y2 = second_position
    if (x2 - 1 == x1 or x2 + 1 == x1) and y1 == y2:
        return True
    if (y2 - 1 == y1 or y2 + 1 == y1) and x1 == x2:
        return True
    return False


def position_on_screen(position):
    x, y = position
    return (x * 50 + 25, y * 50 + 25)


class ScreenMode:
    def __init__(self, active):
        self._active = active

    def active(self):
        return self._active

    def change_active(self):
        self._active = not self.active()

    def background(self, screen):
        screen.fill('bisque')


class TitleScreen(ScreenMode):
    def __init__(self, active=True):
        super().__init__(active)

    def key_function(self, event, menuscreen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.change_active()
                menuscreen.change_active()

    def draw(self, screen, font, jewel):
        self.background(screen)
        jewel_rect = jewel.get_rect(center=(SCREEN_WIDTH/2, 128))
        begin_info = font.render(
            'Press space to start the game',
            True,
            'Blue'
            )
        begin_info_rect = begin_info.get_rect(center=(
            SCREEN_WIDTH/2,
            (SCREEN_HEIGHT + 256) / 2)
            )
        screen.blit(jewel, jewel_rect)
        screen.blit(begin_info, begin_info_rect)


class MenuScreen(ScreenMode):
    def __init__(self, active=False, normal_mode=True, inputing_name=True):
        super().__init__(active)
        self._normal_mode = normal_mode
        self._inputing_name = inputing_name

    def normal_mode(self):
        return self._normal_mode

    def change_normal_mode(self):
        self._normal_mode = not self.normal_mode()

    def inputing_name(self):
        return self._inputing_name

    def change_inputing_name(self):
        self._inputing_name = not self.inputing_name()

    def key_function(self, event, gamescreen, game):
        if self.inputing_name():
            if event.key == pygame.K_BACKSPACE:
                game.set_name(game.name()[:-1])
            elif event.key == pygame.K_SPACE and game.name():
                self.change_inputing_name()
            elif event.key != pygame.K_SPACE:
                game.set_name(game.name() + event.unicode)
        else:
            if event.key == pygame.K_SPACE:
                self.change_inputing_name()
                self.change_active()
                gamescreen.change_active()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                self.change_normal_mode()

    def draw(self, screen, font, game):
        self.background(screen)
        name_info = font.render(
            'Please enter your name. Press space to confirm.',
            True,
            'Black'
        )
        name_info_rect = name_info.get_rect(center=(
            SCREEN_WIDTH/2,
            20
        ))
        mode_info = font.render(
            'Please choose mode of game',
            True,
            'Black'
        )
        mode_info_rect = mode_info.get_rect(center=(
            SCREEN_WIDTH/2,
            60
        ))
        normal_info = font.render(
            'normal',
            True,
            'Blue'
        )
        normal_info_rect = normal_info.get_rect(center=(
            SCREEN_WIDTH/2,
            80
        ))
        endless_info = font.render(
            'endless',
            True,
            'Blue'
        )
        endless_info_rect = endless_info.get_rect(center=(
            SCREEN_WIDTH/2,
            100
        ))
        name_text = font.render(game.name(), True, 'black')
        name_text_rect = name_text.get_rect(center=(
                SCREEN_WIDTH/2,
                40
            ))
        screen.blit(name_text, name_text_rect)
        screen.blit(name_info, name_info_rect)
        if not self.inputing_name():
            screen.blit(mode_info, mode_info_rect)
            screen.blit(normal_info, normal_info_rect)
            screen.blit(endless_info, endless_info_rect)
            if self.normal_mode():
                position = (
                    SCREEN_WIDTH/2-40,
                    70,
                    80,
                    20
                )
            else:
                position = (
                    SCREEN_WIDTH/2-40,
                    90,
                    80,
                    20
                )
            pygame.draw.rect(
                screen,
                'red',
                pygame.Rect(position),
                2
                )


class GameScreen(ScreenMode):
    def __init__(self, active=False, error_time=-1000, cursor=None, select=None, is_sellected=False, is_game_over=False):
        super().__init__(active)
        if cursor is None:
            cursor = [0, 0]
        if select is None:
            select = []
        self._error_time = error_time
        self._cursor = cursor
        self._select = select
        self._is_sellected = is_sellected
        self._is_game_over = is_game_over

    def error_time(self):
        return self._error_time

    def set_error_time(self, new_error_time):
        self._error_time = new_error_time

    def cursor(self):
        return self._cursor

    def set_cursor(self, new_cursor):
        self._cursor = new_cursor

    def select(self):
        return self._select

    def set_sellect(self, new_select):
        self._select = new_select

    def is_sellected(self):
        return self._is_sellected

    def change_is_sellected(self):
        self._is_sellected = not self.is_sellected()

    def is_game_over(self):
        return self._is_game_over

    def change_is_game_over(self):
        self._is_game_over = not self.is_game_over()

    def key_function(self, event, game, board, leaderboard, ending_screen):
        if not self.is_game_over():
            if event.key == pygame.K_SPACE:
                if not self.is_sellected():
                    self.set_sellect(tuple(self.cursor()))
                    self.change_is_sellected()
                elif self.select() != tuple(self.cursor()):
                    self.change_is_sellected()
                    if adjacent(self.select(), self.cursor()):
                        board.swap_jewels(
                            self.select(),
                            self.cursor()
                            )
                        if not board.destroying_move():
                            board.swap_jewels(
                                self.select(),
                                self.cursor()
                                )
                            self.set_error_time(pygame.time.get_ticks())
                        else:
                            game.one_move()
                    else:
                        self.set_error_time(pygame.time.get_ticks())
            if event.key == pygame.K_RIGHT and self.cursor()[0] != board_width - 1:
                self.cursor()[0] += 1
            if event.key == pygame.K_LEFT and self.cursor()[0] != 0:
                self.cursor()[0] -= 1
            if event.key == pygame.K_DOWN and self.cursor()[1] != board_height - 1:
                self.cursor()[1] += 1
            if event.key == pygame.K_UP and self.cursor()[1] != 0:
                self.cursor()[1] -= 1
        else:
            if event.key == pygame.K_SPACE:
                self.change_active()
                ending_screen.change_active()
                leaderboard.adding_new_score(game.name(), game.score())
                leaderboard.set_to_json()
                game.set_name('')

    def automatic(self, board, game):
        if board.game_over(game.moves()):
            self.change_is_game_over()
        board.jewel_refill()
        game.set_score(game.score() + board.destroying_jewels())

    def draw(self, screen, font, game, current_time, board):
        self.background(screen)
        invalid_text = font.render('Invalid move', True, 'Red')
        score = game.score()
        score_text = font.render(
            f'Score: {score}',
            True,
            'Black'
            )

        highscore = score if game.highscore() < game.score() else game.highscore()
        highscore_text = font.render(
            f'Highscore: {highscore}',
            True,
            'Black'
            )

        moves = game.moves()
        moves_text = font.render(
            f'Moves: {moves}',
            True,
            'Black'
        )

        for y in range(board_height):
            for x in range(board_width):
                pygame.draw.ellipse(
                    screen,
                    board.board()[y][x].colour(),
                    pygame.Rect(x*50+10, y*50+10, 40, 40)
                    )
        x, y = position_on_screen(self.cursor())
        pygame.draw.ellipse(screen, 'black', pygame.Rect(x, y, 5, 5))
        screen.blit(score_text, (board_width*50, 10))
        screen.blit(highscore_text, (board_width*50, 60))
        screen.blit(moves_text, (board_width*50, 110))
        if current_time - self.error_time() < 1000:
            screen.blit(invalid_text, (board_width*50, 160))

        if self.is_sellected():
            x, y = position_on_screen(self.select())
            pygame.draw.rect(
                screen,
                'red',
                pygame.Rect(x-20, y-20, 50, 50),
                5
                )


class EndingScreen(ScreenMode):
    def __init__(self, active=False):
        super().__init__(active)

    def key_function(self, event, title_screen):
        if event.key == pygame.K_SPACE:
            self.change_active()
            title_screen.change_active()

    def draw(self, screen, font):
        self.background(screen)
        ending_text = font.render('Game over', True, 'Red')
        ending_text_rect = ending_text.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2
        ))
        screen.blit(ending_text, ending_text_rect)


def interface(board, game, leaderboard):
    pygame.init()
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()

    # fonts
    font = pygame.font.Font('OpenSans.ttf', 12)
    font_title = pygame.font.Font('OpenSans.ttf', 32)
    font_menu = pygame.font.Font('Opensans.ttf', 16)

    jewel = pygame.image.load('jewel.png')
    pygame.display.set_icon(jewel)

    title_screen = TitleScreen()
    menu_screen = MenuScreen()
    game_screen = GameScreen()
    ending_screen = EndingScreen()

    while True:
        current_time = pygame.time.get_ticks()
        if game_screen.active():
            game_screen.automatic(board, game)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if title_screen.active():
                    title_screen.key_function(event, menu_screen)

                elif menu_screen.active():
                    menu_screen.key_function(event, game_screen, game)

                elif game_screen.active():
                    game_screen.key_function(event, game, board, leaderboard, ending_screen)

                else:
                    ending_screen.key_function(event, title_screen)

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # drawing
        if title_screen.active():
            title_screen.draw(screen, font_title, jewel)

        elif menu_screen.active():
            menu_screen.draw(screen, font_menu, game)

        elif game_screen.active():
            game_screen.draw(screen, font, game, current_time, board)

        elif ending_screen.active():
            ending_screen.draw(screen, font_title)

        pygame.display.update()
        clock.tick(30)
