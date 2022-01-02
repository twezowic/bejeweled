import pygame
from sys import exit
from game import Score
from config import (
    board_height,
    board_width,
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


def moving(cursor_position):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and cursor_position[0] != board_width - 1:
        cursor_position[0] += 1
    if keys[pygame.K_LEFT] and cursor_position[0] != 0:
        cursor_position[0] -= 1
    if keys[pygame.K_DOWN] and cursor_position[1] != board_height - 1:
        cursor_position[1] += 1
    if keys[pygame.K_UP] and cursor_position[1] != 0:
        cursor_position[1] -= 1


def interface(board, game, leaderboard):
    pygame.init()
    SCREEN_WIDTH = board_width*50+110
    SCREEN_HEIGHT = board_height*50+10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()

    font = pygame.font.Font('OpenSans.ttf', 12)
    font_title = pygame.font.Font('OpenSans.ttf', 32)
    font_menu = pygame.font.Font('Opensans.ttf', 16)

    jewel = pygame.image.load('jewel.png')
    jewel_rect = jewel.get_rect(center=(SCREEN_WIDTH/2, 128))

    begin_info = font_title.render(
        'Press space to start the game',
        True,
        'Blue'
        )
    begin_info_rect = begin_info.get_rect(center=(
        SCREEN_WIDTH/2,
        (SCREEN_HEIGHT + 256) / 2)
        )

    invalid_move_text = font.render('Invalid move', True, 'Red')
    ending_text = font.render('Game over', True, 'Red')
    ending_text_rect = ending_text.get_rect(center=(
        SCREEN_WIDTH/2,
        SCREEN_HEIGHT/2
        ))

    # menu screen
    player_name = ''
    name_info = font_menu.render(
        'Please enter your name. Press space to confirm.',
        True,
        'Black'
        )
    name_info_rect = name_info.get_rect(center=(
        SCREEN_WIDTH/2,
        20
        ))
    mode_info = font_menu.render(
        'Please choose mode of game',
        True,
        'Black'
        )
    mode_info_rect = mode_info.get_rect(center=(
        SCREEN_WIDTH/2,
        60
        ))
    normal_info = font_menu.render(
        'normal',
        True,
        'Blue'
        )
    normal_info_rect = normal_info.get_rect(center=(
        SCREEN_WIDTH/2,
        80
        ))
    endless_info = font_menu.render(
        'endless',
        True,
        'Blue'
        )
    endless_info_rect = endless_info.get_rect(center=(
        SCREEN_WIDTH/2,
        100
        ))
    mode = False
    normal = True

    pygame.display.set_icon(jewel)

    error_time = -1000

    cursor_position = [0, 0]

    selected_position = []
    select = False

    highscore = leaderboard.get_highscore()

    table = board.board()

    title_screen = True
    menu = False
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if title_screen:
                    if event.key == pygame.K_SPACE:
                        title_screen = False
                        menu = True
                elif menu:
                    if not mode:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode
                    if event.key == pygame.K_SPACE:
                        if mode is False:
                            mode = True
                        else:
                            mode = False
                            menu = False
                            active = True
                    elif event.key == pygame.K_DOWN:
                        normal = False
                    elif event.key == pygame.K_UP:
                        normal = True
                elif not active:
                    if event.key == pygame.K_SPACE:
                        title_screen = True
                else:
                    if event.key == pygame.K_SPACE:
                        # zamiana klejnotow
                        if select is False:
                            select = True
                            selected_position = tuple(cursor_position)
                        elif selected_position != tuple(cursor_position):
                            select = False
                            if adjacent(selected_position, cursor_position):
                                board.swap_jewels(
                                    selected_position,
                                    cursor_position
                                    )
                                if not board.destroying_move():
                                    board.swap_jewels(
                                        selected_position,
                                        cursor_position
                                        )
                                    error_time = pygame.time.get_ticks()
                                else:
                                    game.one_move()
                            else:
                                error_time = pygame.time.get_ticks()
            # zamykanie okna
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('bisque')

        if title_screen:
            screen.blit(jewel, jewel_rect)
            screen.blit(begin_info, begin_info_rect)

        elif menu:
            name_text = font.render(player_name, True, 'black')
            name_text_rect = name_text.get_rect(center=(
                SCREEN_WIDTH/2,
                40
            ))
            screen.blit(name_text, name_text_rect)
            screen.blit(name_info, name_info_rect)
            if mode:
                screen.blit(mode_info, mode_info_rect)
                screen.blit(normal_info, normal_info_rect)
                screen.blit(endless_info, endless_info_rect)
                if normal:
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

        elif active:
            # przygotowanie tekstu
            score = game.score()
            score_text = font.render(
                f'Score: {score}',
                True,
                'Black'
                )

            highscore = score if highscore < score else highscore
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

            # ruchy
            moving(cursor_position)

            # automatyczne działania na planszy
            if board.game_over(game.moves()):
                active = False
                leaderboard.adding_new_score(Score(player_name, score))
                leaderboard.set_to_json()
                player_name = ''
            board.jewel_refill()
            game.set_score(score + board.destroying_jewels())

            current_time = pygame.time.get_ticks()

            # rysowanie
            for y in range(board_height):
                for x in range(board_width):
                    pygame.draw.ellipse(
                        screen,
                        table[y][x].colour(),
                        pygame.Rect(x*50+10, y*50+10, 40, 40)
                        )
            x, y = position_on_screen(cursor_position)
            pygame.draw.ellipse(screen, 'black', pygame.Rect(x, y, 5, 5))
            screen.blit(score_text, (board_width*50, 10))
            screen.blit(highscore_text, (board_width*50, 60))
            screen.blit(moves_text, (board_width*50, 110))
            if current_time - error_time < 1000:
                screen.blit(invalid_move_text, (board_width*50, 160))

            if select:
                x, y = position_on_screen(selected_position)
                pygame.draw.rect(
                    screen,
                    'red',
                    pygame.Rect(x-20, y-20, 50, 50),
                    5
                    )

        else:
            screen.blit(ending_text, ending_text_rect)

        pygame.display.update()
        clock.tick(10)
