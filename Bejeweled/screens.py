import pygame
from time import sleep


class ScreenMode:
    def __init__(self, width: int, height: int, active: bool):
        """
        Creates instance of ScreenMode class.

        Args:
            width (int): screen's width

            height (int): screen's height

            active (bool): is the screen displayed
        """
        self._width = width
        self._height = height
        self._active = active

    def width(self) -> int:
        """
        Returns:
            int: screen's width
        """
        return self._width

    def height(self) -> int:
        """
        Returns:
            int: screen's height
        """
        return self._height

    def active(self) -> bool:
        """
        Returns:
            bool: is the screen displayed
        """
        return self._active

    def change_active(self):
        """
        Changes is the active attribute is True or False.
        If it is True it changes it to False.
        And if it is False it changes it to True.
        """
        self._active = not self.active()

    def background(self, screen):
        """
        Fills the background of the screen with bisque colour.

        Args:
            screen (pygame.display): screen in which it will be displayed
        """
        screen.fill('bisque')


class TitleScreen(ScreenMode):
    def __init__(self, width: int, height: int):
        """
        Creates instance of TitleScreen class.
        Which inherits from ScreenMode class.

        Args:
            width (int): screen's width

            height (int): screen's height

            active (bool): is the screen displayed.
            Defaults to True.
        """
        super().__init__(width, height, True)

    def key_function(self, event, menuscreen):
        """
        Adds key functionality to interface.

        If space is pressed the active screen is changed.
        From TitleScreen to ModeScreen by changing the active attributes.


        Args:
            event (pygame.event): event object from pygame

            menuscreen (Menuscreen): menuscreen object
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.change_active()
                menuscreen.change_active()

    def draw(self, screen, font, jewel):
        """
        Prepares the title screen for displaying.

        Args:
            screen (pygame.display): screen in which it will be displayed

            font (pygame.font): font which is being used

            jewel (image): image which will be displayed
        """
        self.background(screen)
        jewel_rect = jewel.get_rect(center=(
            self.width()*0.5,
            self.height() * 0.4))
        begin_info = font.render(
            'Press space to start the game',
            True,
            'Blue'
            )
        begin_info_rect = begin_info.get_rect(center=(
            self.width() * 0.5,
            self.height() * 0.75
            ))
        screen.blit(jewel, jewel_rect)
        screen.blit(begin_info, begin_info_rect)


class MenuScreen(ScreenMode):
    def __init__(
            self,
            width: int,
            height: int):
        """
        Creates instance of MenuScreen class
        Which inherits from ScreenMode class.

        Args:
            width (int): screen's width

            height (int): screen's height

            active (bool): is the screen displayed.
            Defaults to False.

            inputing_name (bool): is in state of inputing name.
            Defaults to True.
        """
        super().__init__(width, height, False)
        self._inputing_name = True

    def inputing_name(self) -> bool:
        """
        Returns:
            bool: is in state of inputing name
        """
        return self._inputing_name

    def change_inputing_name(self):
        """
        Changes is the inputing_name attribute is True or False.
        If it is True it changes it to False.
        And if it is False it changes it to True.
        """
        self._inputing_name = not self.inputing_name()

    def key_function(self, event, gamescreen, game):
        """
        Adds key functionality to interface.

        If game is in inputing state:
            If backspace is pressed:
            The game.score().delete_letter() method is performed.

            If space is pressed and player's name is not empty:
            The self.change_inputing_name method is performed.

            Otherwise:
            The game.score().add_letter(key) method is performed.
            Where key is what key was pressed.

        Otherwise:
            If space is pressed the active screen is changed.
            From ModeScreen to GameScreen by changing the active attributes.
            Resets the inputing_name attribute.
            The game.board().create_board() method is performed.

            If up arrow or down arrow method is pressed.
            The game.level().change_mode() method is performed

        Args:
            event (pygame.event): event object from pygame

            gamescreen (GameScreen): object of GameScreen class

            game (Game): object of Game class
        """
        if self.inputing_name():
            if event.key == pygame.K_BACKSPACE:
                game.score().delete_letter()
            elif event.key == pygame.K_SPACE and game.score().name():
                self.change_inputing_name()
            else:
                game.score().add_letter(event.unicode)
        else:
            if event.key == pygame.K_SPACE:
                self.change_inputing_name()
                self.change_active()
                gamescreen.change_active()
                game.setup_board()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                game.level().change_mode()

    def draw(self, screen, font, game):
        """
        Prepares the menu screen for displaying.

        Args:
            screen (pygame.display): screen in which it will be displayed

            font (pygame.font): font which is being used

            game (Game): object of Game class
        """
        self.background(screen)
        name_info = font.render(
            'Please enter your name. Press space to confirm.',
            True,
            'Black'
        )
        name_info_rect = name_info.get_rect(center=(
            self.width()/2,
            20
        ))
        mode_info = font.render(
            'Please choose mode of game',
            True,
            'Black'
        )
        mode_info_rect = mode_info.get_rect(center=(
            self.width()/2,
            60
        ))
        normal_info = font.render(
            'normal',
            True,
            'Blue'
        )
        normal_info_rect = normal_info.get_rect(center=(
            self.width()/2,
            80
        ))
        endless_info = font.render(
            'endless',
            True,
            'Blue'
        )
        endless_info_rect = endless_info.get_rect(center=(
            self.width()/2,
            100
        ))
        name_text = font.render(game.score().name(), True, 'black')
        name_text_rect = name_text.get_rect(center=(
                self.width()/2,
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
                    self.width()/2-40,
                    70,
                    80,
                    20
                )
            else:
                position = (
                    self.width()/2-40,
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
            width: int,
            height: int):
        """
        Creates instance of GameScreen class.
        Which inherits from ScreenMode class.

        Args:
            width (int): screen's width

            height (int): screen's height

            active (bool): is the screen displayed
            Defaults to False.

            error_time (int): time when a invalid move is done.
            Default number is set to -1000 so,
                the error message wouldn't be showed at the start.
            Defaults to -1000.

            cursor (list): cursor positon in board scale.
            Defaults to [0, 0].

            select (list): selected jewel position.
            Defaults to [].

            is_sellected (bool): is jewel sellected.
            Defaults to False.

            is_game_over (bool): is game in game over state.
            Defaults to False.

            is_win (bool): is game in win state.
            Defaults to False.

            is_automatic (bool): is automatic function of board being held.
            Defaults to False.

            highscore (int): the best player's score of this game.
            Defaults to 0.
        """

        super().__init__(width, height, False)
        self._error_time = -1000
        self._cursor = [0, 0]
        self._select = []
        self._is_sellected = False
        self._is_game_over = False
        self._is_win = False
        self._is_automatic = False
        self._highscore = 0

    def error_time(self) -> int:
        """
        Returns:
            int: time when a invalid move is done.
        """
        return self._error_time

    def set_error_time(self, new_error_time: int):
        """
        Sets when the invalid move is done.

        Args:
            new_error_time (int): time of error to be set
        """
        self._error_time = new_error_time

    def cursor(self) -> list:
        """
        Returns:
            list: cursor positon in board scale.
        """
        return self._cursor

    def set_cursor(self, new_cursor: list):
        """
        Sets cursor position

        Args:
            new_cursor (list): cursor positon to be set
        """
        self._cursor = new_cursor

    def select(self) -> list:
        """
        Returns:
            list: selected jewel position
        """
        return self._select

    def set_sellect(self, new_select: list):
        """
        Sets sellected jewel position

        Args:
            new_select (list): sellected jewel position to be set
        """
        self._select = new_select

    def is_sellected(self) -> bool:
        """
        Returns:
            bool: is jewel sellected.
        """
        return self._is_sellected

    def change_is_sellected(self):
        """
        Changes is the is_sellected attribute is True or False.
        If it is True it changes it to False.
        And if it is False it changes it to True.
        """
        self._is_sellected = not self.is_sellected()

    def is_game_over(self) -> bool:
        """
        Returns:
            bool: is game in game over state.
        """
        return self._is_game_over

    def change_is_game_over(self):
        """
        Changes is the is_game_over attribute is True or False.
        If it is True it changes it to False.
        And if it is False it changes it to True.
        """
        self._is_game_over = not self.is_game_over()

    def is_win(self) -> bool:
        """
        Returns:
            bool: is game in win state
        """
        return self._is_win

    def change_is_win(self):
        """
        Changes is the is_win attribute is True or False.
        If it is True it changes it to False.
        And if it is False it changes it to True.
        """
        self._is_win = not self.is_win()

    def is_automatic(self) -> bool:
        """
        Returns:
            bool: is automatic function of board being held
        """
        return self._is_automatic

    def set_is_automatic(self, new_is_automatic: bool):
        """
        Sets is automatic function of board being held.

        Args:
            new_is_automatic (bool): automatic state to be set
        """
        self._is_automatic = new_is_automatic

    def highscore(self) -> int:
        """
        Returns:
            int: the best player's score of this game
        """
        return self._highscore

    def set_highscore(self, new_highscore: int):
        """
        Sets new highscore of this game.

        Args:
            new_highscore (int): highscore to be set
        """
        self._highscore = new_highscore

    def key_function(self, event, ending_screen, game):
        """
        Adds key functionality to interface.

        If game is in win state:
            If space is pressed:
            The is_win attribute reset.
            The game.next_level() method is performed.

            If e is pressed the active screen is changed:
            From ModeScreen to GameScreen by changing the active attributes.
            Gamescreen resets.
            The score is added to the leaderboard and saved to file.

        If game is in game_over state:
            If space is pressed the active screen is changed:
            From ModeScreen to GameScreen by changing the active attributes.
            Gamescreen resets.
            The score is added to the leaderboard and saved to file.

        if game not in automatic state:
            If space is pressed:
            The jewel is sellected if it was not.
            Otherwise game.moving_jewels() method is performed

            If right key is pressed:
            The cursor position moves to the right not outside of board.

            If left key is pressed:
            The cursor position moves to the left not outside of board.

            If up key is pressed:
            The cursor position moves to the up not outside of board.

            If down key is pressed:
            The cursor position moves to the down not outside of board.

            If e is pressed and game is endless mode:
            The self.change_is_game_over() method is performed.

        Args:
            event (pygame.event): event object from pygame

            ending_screen (EndingScreen): object of EndingScreen class

            game (Game): object of Game class
        """
        if self.is_win():
            if event.key == pygame.K_SPACE:
                self.change_is_win()
                game.next_level()
            elif event.key == pygame.K_e:
                self.change_active()
                ending_screen.change_active()
                self.change_is_win()
                game_mode = game.level().mode()
                game.score().set_score(self.highscore())
                game.leaderboard().adding_new_score(
                    game.score(),
                    game_mode
                    )
                game.leaderboard().save_to_file()
        elif self.is_game_over():
            if event.key == pygame.K_SPACE:
                self.change_active()
                self.change_is_game_over()
                ending_screen.change_active()
                game_mode = game.level().mode()
                game.score().set_score(self.highscore())
                game.leaderboard().adding_new_score(
                    game.score(),
                    game_mode
                    )
                game.leaderboard().save_to_file()
        elif not self.is_automatic():
            if event.key == pygame.K_SPACE:
                if not self.is_sellected():
                    self.set_sellect(tuple(self.cursor()))
                else:
                    if not game.moving_jewels(self.cursor(), self.select()):
                        self.set_error_time(pygame.time.get_ticks())
                self.change_is_sellected()

            elif event.key == pygame.K_RIGHT:
                if self.cursor()[0] != game.board().width() - 1:
                    self.cursor()[0] += 1
            elif event.key == pygame.K_LEFT:
                if self.cursor()[0] != 0:
                    self.cursor()[0] -= 1
            elif event.key == pygame.K_DOWN:
                if self.cursor()[1] != game.board().height() - 1:
                    self.cursor()[1] += 1
            elif event.key == pygame.K_UP:
                if self.cursor()[1] != 0:
                    self.cursor()[1] -= 1
            elif event.key == pygame.K_e:
                if not game.level().is_normal():
                    self.change_is_game_over()

    def automatic(self, game):
        """
        Performs automatic functions:

        If there are blank jewels in board:
        The game.board().jewel_refill() method is performed.

        If there are jewels to destroy:
        The game.destroying_jewels(True) method is performed.

        If the win condition is fulfilled:
        The self.change_win() method is performed.

        If the game over condition is fulfilled:
        The self.change_game_over() method is performed.

        Args:
            game (Game): object of Game class

        Returns:
            bool: is automatic board functions is done
        """
        if game.board().is_blank():
            game.board().jewel_refill()
            self.set_is_automatic(True)
            sleep(0.5)
            return True
        elif game.board().destroying_move():
            game.destroying_jewels(True)
            self.set_is_automatic(True)
            sleep(0.5)
            return True
        elif game.level().win_condition(game.score().score()):
            if not self.is_win():
                self.change_is_win()
        if game.board().game_over(game.level().moves(), game.level().mode()):
            if not self.is_game_over():
                self.change_is_game_over()
        self.set_is_automatic(False)

    def draw(self, screen, font, game, current_time):
        """
        Prepares the game screen for displaying.

        Args:
            screen (pygame.display): screen in which it will be displayed

            font (pygame.font): font which is being used

            game (Game): object of Game class

            current_time (int): current time of game
        """

        def position_on_screen_cursors(position: list) -> list:
            """
            Args:
                position (list): position of cursor in board scale

            Returns:
                list: position of cursor in screen scale
            """
            x, y = position
            return (x * 50 + 30, y * 50 + 30)

        def position_on_screen_select(position: list) -> list:
            """
            Args:
                position (list): position of sellected jewel in board scale

            Returns:
                list: position of sellected jewel in screen scale
            """
            x, y = position
            return (x*50+5, y*50+5)

        def position_on_screen_jewels(position: list) -> list:
            """
            Args:
                position (list): position of jewel in board scale

            Returns:
                list: points of jewel to display on screen
            """
            x, y = position
            return (
                (20+x*50, 15+y*50),
                (40+x*50, 15+y*50),
                (50+x*50, 30+y*50),
                (30+x*50, 50+y*50),
                (10+x*50, 30+y*50)
            )

        menu_width = self.width() - 100

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
        if self.highscore() < game.score().score():
            self.set_highscore(game.score().score())
        if game.leaderboard().highscore(game_mode) < self.highscore():
            highscore = self.highscore()
        else:
            highscore = game.leaderboard().highscore(game_mode)
        highscore_text = font.render(
            f'Highscore: {highscore}',
            True,
            'Black'
            )
        highscore_height = 210 if game.level().is_normal() else 110
        highscore_rect = highscore_text.get_rect(topleft=(
            menu_width,
            highscore_height
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

        exit_text = font.render(
            'Press e to exit.',
            True,
            'Black'
        )
        if game.level().is_normal():
            exit_rect = exit_text.get_rect(center=(
                (self.width()-110)/2,
                (self.height()+30)/2
            ))
        else:
            exit_rect = exit_text.get_rect(topleft=(
                menu_width,
                210
            ))

        invalid_text = font.render('Invalid move', True, 'Red')
        invalid_rect = invalid_text.get_rect(topleft=(
            self.width() - 100,
            260
        ))

        white_box = pygame.Surface((200, 50))
        white_box.fill('white')
        white_box_rect = white_box.get_rect(center=(
            (self.width()-110)/2,
            self.height()/2
        ))
        reason = 'Game over'
        if game.level().is_normal():
            if game.level().moves() == 0:
                reason = f'No moves left. {reason}'
            else:
                reason = f'No moves available. {reason}'

        game_over = font.render(
            reason,
            True,
            'Red'
        )
        game_over_rect = game_over.get_rect(center=(
            (self.width()-110)/2,
            (self.height()-10)/2
        ))

        info = font.render(
            'Press space to continue',
            True,
            'Black'
        )
        info_rect = info.get_rect(center=(
            (self.width()-110)/2,
            (self.height()+10)/2
        ))

        win = font.render(
            'Level complete',
            True,
            'Blue'
        )
        win_rect = win.get_rect(center=(
            (self.width()-110)/2,
            (self.height()-10)/2
        ))

        self.background(screen)
        for y in range(game.board().height()):  # diamonds
            for x in range(game.board().width()):
                pygame.draw.polygon(
                    screen,
                    game.board().board()[y][x].colour(),
                    position_on_screen_jewels((x, y))
                )

        if not self.is_game_over() and not self.is_win():
            if not self.is_automatic():
                pygame.draw.circle(  # ramka
                    screen,
                    'black',
                    position_on_screen_cursors(self.cursor()),
                    24,
                    4
                    )

        screen.blit(score_text, score_rect)
        screen.blit(highscore_text, highscore_rect)
        if game.level().is_normal():
            screen.blit(score_goal_text, score_goal_rect)
            screen.blit(level_text, level_rect)
            screen.blit(moves_text, moves_rect)
        else:
            screen.blit(exit_text, exit_rect)

        if current_time - self.error_time() < 1000:
            screen.blit(invalid_text, invalid_rect)

        if self.is_sellected():
            x, y = position_on_screen_select(self.select())
            pygame.draw.rect(
                screen,
                'black',
                pygame.Rect(x, y, 50, 50),
                5
                )

        if self.is_win():
            screen.blit(white_box, white_box_rect)
            screen.blit(win, win_rect)
            screen.blit(info, info_rect)
            screen.blit(exit_text, exit_rect)
        elif self.is_game_over():
            screen.blit(white_box, white_box_rect)
            screen.blit(game_over, game_over_rect)
            screen.blit(info, info_rect)


class EndingScreen(ScreenMode):
    def __init__(self, width: int, height: int):
        """
        Creates instance of EndingScreen class.
        Which inherits from ScreenMode class.

        Args:
            width (int): screen's width

            height (int): screen's height

            active (bool): is the screen displayed.
        """
        super().__init__(width, height, False)

    def key_function(self, event, title_screen, game):
        """
        Adds key functionality to interface.

        If space is pressed the active screen is changed.
        From EndingScreen to TitleScreen by changing the active attributes.

        Args:
            event (pygame.event): event object from pygame

            title_screen (TitleScreen): object of TitleScreen class

            game (Game): object of Game class
        """
        if event.key == pygame.K_SPACE:
            self.change_active()
            game.reset()
            title_screen.change_active()

    def draw(self, screen, font, game):
        """
        Prepares the ending screen for displaying.

        Args:
            screen (pygame.display): screen in which it will be displayed

            font (pygame.font): font which is being used

            game (Game): object of Game class
        """
        self.background(screen)
        ending_text = font.render('Leaderboard', True, 'Blue')
        ending_text_rect = ending_text.get_rect(center=(
            self.width()/2,
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
