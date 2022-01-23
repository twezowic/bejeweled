import pygame
from sys import exit
from bejeweled.screens import TitleScreen, MenuScreen, GameScreen, EndingScreen


def interface(game):
    """
    Shows interface created in screens.py file.

    Args:
        game (Game): object of Game class
    """
    pygame.init()
    SCREEN_WIDTH = game.board().width()*50+110
    SCREEN_HEIGHT = game.board().height()*50+10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()

    font_path = 'Bejeweled/download/Opensans.ttf'
    font = pygame.font.Font(font_path, 12)
    font_title = pygame.font.Font(font_path, 32)
    font_menu = pygame.font.Font(font_path, 16)

    jewel = pygame.image.load('Bejeweled/download/jewel.png')
    pygame.display.set_icon(jewel)

    title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    menu_screen = MenuScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    ending_screen = EndingScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        current_time = pygame.time.get_ticks()

        if game_screen.active():
            game_screen.automatic(game)

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
                        ending_screen,
                        game
                        )

                else:
                    ending_screen.key_function(
                        event,
                        title_screen,
                        game
                        )

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if title_screen.active():
            title_screen.draw(screen, font_title, jewel)

        elif menu_screen.active():
            menu_screen.draw(screen, font_menu, game)

        elif game_screen.active():
            game_screen.draw(screen, font, game, current_time)

        elif ending_screen.active():
            ending_screen.draw(screen, font_title, game)

        pygame.display.update()
        clock.tick(30)
