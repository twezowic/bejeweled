import pygame
from config import (
    board_height,
    board_width,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    )
from time import sleep


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
    return (x * 50 + 30, y * 50 + 30)


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
    def __init__(self, active=False, inputing_name=True):
        super().__init__(active)
        self._inputing_name = inputing_name

    def inputing_name(self):
        return self._inputing_name

    def change_inputing_name(self):
        self._inputing_name = not self.inputing_name()

    def key_function(self, event, gamescreen, game):
        if self.inputing_name():
            if event.key == pygame.K_BACKSPACE:
                game.score().delete_letter()
            elif event.key == pygame.K_SPACE and game.score().name():
                self.change_inputing_name()
            elif event.key != pygame.K_SPACE:
                game.score().add_letter(event.unicode)
        else:
            if event.key == pygame.K_SPACE:
                self.change_inputing_name()
                self.change_active()
                gamescreen.change_active()
                game.board().setup_board()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                game.level().change_mode()

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
        name_text = font.render(game.score().name(), True, 'black')
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
            if game.level().is_normal():
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
    def __init__(
            self,
            active=False,
            error_time=-1000,
            cursor=None,
            select=None,
            is_sellected=False,
            is_game_over=False,
            is_win=False):

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
        self._is_win = is_win

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

    def is_win(self):
        return self._is_win

    def change_is_win(self):
        self._is_win = not self.is_win()

    def key_function(self, event, game, ending_screen):
        if self.is_win():
            if event.key == pygame.K_SPACE:
                self.change_is_win()
                game.next_level()
        elif self.is_game_over():
            if event.key == pygame.K_SPACE:
                self.change_active()
                self.change_is_game_over()
                ending_screen.change_active()
                game_mode = game.level().mode()
                game.leaderboard().adding_new_score(
                    game.score(),
                    game_mode
                    )
                game.leaderboard().save(game_mode)
        else:
            if event.key == pygame.K_SPACE:
                if not self.is_sellected():
                    self.set_sellect(tuple(self.cursor()))
                    self.change_is_sellected()
                elif self.select() != tuple(self.cursor()):
                    self.change_is_sellected()
                    if adjacent(self.select(), self.cursor()):
                        game.board().swap_jewels(
                            self.select(),
                            self.cursor()
                            )
                        if not game.board().destroying_move():
                            game.board().swap_jewels(
                                self.select(),
                                self.cursor()
                                )
                            self.set_error_time(pygame.time.get_ticks())
                        elif game.level().is_normal():
                            game.level().one_move()
                    else:
                        self.set_error_time(pygame.time.get_ticks())
            elif event.key == pygame.K_RIGHT:
                if self.cursor()[0] != board_width - 1:
                    self.cursor()[0] += 1
            elif event.key == pygame.K_LEFT:
                if self.cursor()[0] != 0:
                    self.cursor()[0] -= 1
            elif event.key == pygame.K_DOWN:
                if self.cursor()[1] != board_height - 1:
                    self.cursor()[1] += 1
            elif event.key == pygame.K_UP:
                if self.cursor()[1] != 0:
                    self.cursor()[1] -= 1
            elif event.key == pygame.K_e:
                if not game.level().is_normal():
                    self.change_is_game_over()

    def automatic(self, game):
        if game.board().is_blank():
            game.board().jewel_refill()
            sleep(0.75)
        elif game.board().destroying_move():
            game.board().destroying_jewels(game)
            sleep(0.5)
        elif game.level().win_condition(game.score().score()):
            if not self.is_win():
                self.change_is_win()
        if game.board().game_over(game.level().moves(), game.level().mode()):
            if not self.is_game_over():
                self.change_is_game_over()

    def draw(self, screen, font, game, current_time):

        menu_width = SCREEN_WIDTH - 100

        score = game.score().score()
        score_text = font.render(
            f'Score: {score}',
            True,
            'Black'
            )
        score_rect = score_text.get_rect(topleft=(
            menu_width,
            10
        ))

        score_goal = game.level().goal()
        score_goal_text = font.render(
            f'Goal: {score_goal}',
            True,
            'Black'
        )
        score_goal_rect = score_goal_text.get_rect(topleft=(
            menu_width,
            60
        ))
        game_mode = game.level().mode()
        if game.leaderboard().highscore(game_mode) < game.score().score():
            highscore = score
        else:
            highscore = game.leaderboard().highscore(game_mode)
        highscore_text = font.render(
            f'Highscore: {highscore}',
            True,
            'Black'
            )
        highscore_rect = highscore_text.get_rect(topleft=(
            menu_width,
            60
        ))

        moves = game.level().moves()
        moves_text = font.render(
            f'Moves: {moves}',
            True,
            'Black'
        )
        moves_rect = moves_text.get_rect(topleft=(
            menu_width,
            160
        ))

        level = game.level().level()
        level_text = font.render(
            f'Level: {level}',
            True,
            'Black'
        )
        level_rect = level_text.get_rect(topleft=(
            menu_width,
            110
        ))

        endless_text = font.render(
            'Press e to exit.',
            True,
            'Black'
        )
        endless_rect = endless_text.get_rect(topleft=(
            menu_width,
            110
        ))

        invalid_text = font.render('Invalid move', True, 'Red')
        invalid_rect = invalid_text.get_rect(topleft=(
            SCREEN_WIDTH - 100,
            260
        ))

        white_box = pygame.Surface((200, 50))
        white_box.fill('white')
        white_box_rect = white_box.get_rect(center=(
            (SCREEN_WIDTH-110)/2,
            SCREEN_HEIGHT/2
        ))
        if game.level().moves() == 0:
            reason = 'No moves left.'
        else:
            reason = 'No moves available.'
        game_over = font.render(
            f'{reason} Game over',
            True,
            'Red'
        )
        game_over_rect = game_over.get_rect(center=(
            (SCREEN_WIDTH-110)/2,
            (SCREEN_HEIGHT-10)/2
        ))

        info = font.render(
            'Press space to continue',
            True,
            'Black'
        )
        info_rect = info.get_rect(center=(
            (SCREEN_WIDTH-110)/2,
            (SCREEN_HEIGHT+10)/2
        ))

        win = font.render(
            'Level complete',
            True,
            'Blue'
        )
        win_rect = win.get_rect(center=(
            (SCREEN_WIDTH-110)/2,
            (SCREEN_HEIGHT-10)/2
        ))
        self.background(screen)
        for y in range(board_height):
            for x in range(board_width):
                pygame.draw.circle(
                    screen,
                    game.board().board()[y][x].colour(),
                    position_on_screen((x, y)),
                    20
                    )

        if not self.is_game_over() and not self.is_win():
            pygame.draw.circle(  # ramka
                screen,
                'black',
                position_on_screen(self.cursor()),
                24,
                4
                )

        screen.blit(score_text, score_rect)

        if game.level().is_normal():
            screen.blit(score_goal_text, score_goal_rect)
            screen.blit(level_text, level_rect)
            screen.blit(moves_text, moves_rect)
        else:
            screen.blit(endless_text, endless_rect)
            screen.blit(highscore_text, highscore_rect)

        if current_time - self.error_time() < 1000:
            screen.blit(invalid_text, invalid_rect)

        if self.is_sellected():
            x, y = position_on_screen(self.select())
            pygame.draw.rect(
                screen,
                'black',
                pygame.Rect(x-25, y-25, 50, 50),
                5
                )

        if self.is_win():
            screen.blit(white_box, white_box_rect)
            screen.blit(win, win_rect)
            screen.blit(info, info_rect)
        elif self.is_game_over():
            screen.blit(white_box, white_box_rect)
            screen.blit(game_over, game_over_rect)
            screen.blit(info, info_rect)


class EndingScreen(ScreenMode):
    def __init__(self, active=False):
        super().__init__(active)

    def key_function(self, event, title_screen, game):
        if event.key == pygame.K_SPACE:
            self.change_active()
            game.reset()
            title_screen.change_active()

    def draw(self, screen, font, game):
        self.background(screen)
        ending_text = font.render('Leaderboard', True, 'Blue')
        ending_text_rect = ending_text.get_rect(center=(
            SCREEN_WIDTH/2,
            30
        ))

        screen.blit(ending_text, ending_text_rect)

        selected = False
        game_mode = game.level().mode()
        for index, score in enumerate(game.leaderboard().scores(game_mode)):
            if game.score() == score and not selected:
                colour = 'red'
                selected = True
            else:
                colour = 'black'
            name_text = font.render(
                f'{index+1:2}. {score.name()}',
                True,
                colour
                )

            score_text = font.render(
                f'{score.score():<10}',
                True,
                colour
            )
            screen.blit(
                name_text,
                (10, 60 + index * 32)
            )
            screen.blit(
                score_text,
                (250, 60 + index * 32)
            )
