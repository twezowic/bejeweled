import pygame
from sys import exit
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
    screen = pygame.display.set_mode((board_width*50+110, board_height*50+10))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()
    test_font = pygame.font.Font(None, 16)  # czcionka, rozmiar

    cursor = pygame.Surface((5, 5))
    cursor.fill('black')
    cursor_position = [0, 0]

    selected_position = []
    select = False

    score = 0
    highscore = get_highscore()

    table = board.board()

    while True:
        for event in pygame.event.get():
            # zamiana klejnotow
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if select is False:
                        select = True
                        selected_position = tuple(cursor_position)
                    elif selected_position != tuple(cursor_position):
                        select = False
                        if adjacent(selected_position, cursor_position):
                            player.one_move()
                            board.swap_jewels(
                                selected_position,
                                cursor_position
                                )
            # zamykanie okna
            if event.type == pygame.QUIT:
                pygame.quit()
                new_highscore(highscore)
                exit()

        if player.moves() > 0:
            moving(cursor_position)
            score = board.destroying_jewels(score)
            score_text = test_font.render(f'Score: {score}', False, 'Black')
            highscore = score if highscore < score else highscore
            highscore_text = test_font.render(
                f'Highscore: {highscore}',
                False,
                'Black'
                )
            moves = player.moves()
            moves_text = test_font.render(f'Moves: {moves}', False, 'Black')
            board.falling_jewels()
            board.new_jewels()

            screen.fill('bisque')
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
            if select:
                x, y = position_on_screen(selected_position)
                pygame.draw.rect(
                    screen,
                    'red',
                    pygame.Rect(x-20, y-20, 50, 50),
                    5
                    )

        else:
            screen.fill('red')
        # odswierzanie ekranu
        pygame.display.update()
        clock.tick(10)
