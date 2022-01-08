import pygame
from sys import exit

from screens import SCREEN_WIDTH, SCREEN_HEIGHT
from screens import TitleScreen, MenuScreen, GameScreen, EndingScreen


def interface(board, game, leaderboard):
    pygame.init()
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
                    title_screen.key_function(
                        event,
                        menu_screen
                        )

                elif menu_screen.active():
                    menu_screen.key_function(
                        event,
                        game_screen,
                        game
                        )

                elif game_screen.active():
                    game_screen.key_function(
                        event,
                        game,
                        board,
                        leaderboard,
                        ending_screen
                        )

                else:
                    ending_screen.key_function(
                        event,
                        title_screen,
                        game,
                        board
                        )

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
            ending_screen.draw(screen, font_title, leaderboard, game)

        pygame.display.update()
        clock.tick(30)
