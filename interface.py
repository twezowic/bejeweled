import pygame
from sys import exit
from config import (
    board_height,
    board_width,
    )


def interface(board):
    pygame.init()
    screen = pygame.display.set_mode((board_width*50+10, board_height*50+10))
    pygame.display.set_caption('Bejeweled')
    clock = pygame.time.Clock()

    cursor = pygame.Surface((5, 5))
    cursor.fill('white')
    cursor_position = [25, 25]
    cursor_position_in_table = [0, 0]

    selected_position = []
    select = False

    table = board.board()

    while True:
        for event in pygame.event.get():

            # zamiana klejnotow
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if select is False:
                        select = True
                        selected_position = tuple(cursor_position_in_table)
                    elif selected_position != tuple(cursor_position_in_table):
                        select = False
                        board.swap_jewels(
                            selected_position,
                            cursor_position_in_table
                            )

            # zamykanie okna
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('white')

        # rysowanie klejnotow
        for y in range(board_height):
            for x in range(board_width):
                pygame.draw.ellipse(
                    screen,
                    table[y][x].colour(),
                    pygame.Rect(x*50+10, y*50+10, 40, 40)
                    )
        # rysowanie ramki wokol wybranego klejnotu
        if select:
            x, y = selected_position
            x *= 50
            y *= 50
            pygame.draw.rect(screen, 'red', pygame.Rect(x+5, y+5, 50, 50), 5)

        # poruszanie sie strzalkami
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if cursor_position[0] != board_width * 50 - 25:
                cursor_position_in_table[0] += 1
                cursor_position[0] += 50
        if keys[pygame.K_LEFT]:
            if cursor_position[0] != 25:
                cursor_position_in_table[0] -= 1
                cursor_position[0] -= 50
        if keys[pygame.K_DOWN]:
            if cursor_position[1] != board_height * 50 - 25:
                cursor_position_in_table[1] += 1
                cursor_position[1] += 50
        if keys[pygame.K_UP]:
            if cursor_position[1] != 25:
                cursor_position_in_table[1] -= 1
                cursor_position[1] -= 50
        screen.blit(cursor, (cursor_position))

        # odswierzanie ekranu
        pygame.display.update()
        clock.tick(15)
