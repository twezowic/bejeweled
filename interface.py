from numpy import cumproduct
import pygame
from sys import exit
from time import sleep
from game import get_highscore, new_highscore
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


def interface(board, player):
    pygame.init()
    SCREEN_WIDTH = board_width*50+110
    SCREEN_HEIGHT = board_height*50+10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()
    font = pygame.font.Font('OpenSans.ttf', 12)
    font_begin = pygame.font.Font('OpenSans.ttf', 32)


    jewel = pygame.image.load('jewel.png')
    jewel_rect = jewel.get_rect(center = (SCREEN_WIDTH/2, 128))
    begin_info = font_begin.render('Press space to start the game', True, 'Blue')
    begin_info_rect = begin_info.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT + 256) / 2))

    pygame.display.set_icon(jewel)

    error_time = -2000

    title_screen = True

    cursor = pygame.Surface((5, 5))
    cursor.fill('black')
    cursor_position = [0, 0]

    selected_position = []
    select = False

    highscore = get_highscore()

    table = board.board()

    invalid_move_text = font.render('Invalid move', False, 'Red')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if title_screen:
                        title_screen = False
                    else:
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
                                    player.one_move()
                if event.key == pygame.K_h:
                    print('help')
                if event.key == pygame.K_l:
                    print('leaderboard')
            # zamykanie okna
            if event.type == pygame.QUIT:
                pygame.quit()
                new_highscore(highscore)
                exit()
        screen.fill('bisque')
        if title_screen:
            screen.blit(jewel, jewel_rect)
            screen.blit(begin_info, begin_info_rect)
        elif player.moves() > 0:
            score = player.score()
            score_text = font.render(f'Score: {score}', True, 'Black')
            highscore = score if highscore < score else highscore
            highscore_text = font.render(
                f'Highscore: {highscore}',
                True,
                'Black'
                )
            moving(cursor_position)
            player.set_score(score + board.destroying_jewels())
            moves = player.moves()
            moves_text = font.render(f'Moves: {moves}', True, 'Black')
            board.jewel_refill()

            current_time = pygame.time.get_ticks()

            for y in range(board_height):
                for x in range(board_width):
                    pygame.draw.ellipse(
                        screen,
                        table[y][x].colour(),
                        pygame.Rect(x*50+10, y*50+10, 40, 40)
                        )
            screen.blit(cursor, (position_on_screen(cursor_position)))
            screen.blit(score_text, (board_width*50, 10))
            screen.blit(highscore_text, (board_width*50, 60))
            screen.blit(moves_text, (board_width*50, 110))
            if current_time - error_time < 2000:
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
            title_screen = True
        # odswierzanie ekranu
        pygame.display.update()
        clock.tick(10)
