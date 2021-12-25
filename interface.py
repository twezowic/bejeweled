import pygame
from sys import exit
from config import (
    board_height,
    board_width,
    )


def interface(board):
    pygame.init()
    screen = pygame.display.set_mode((board_width*50, board_height*50))
    jewel = pygame.Surface((50, 50))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bejeweled')

    cursor = pygame.Surface((5, 5))
    cursor.fill('white')
    cursor_position = [25, 25]
    cursor_position_in_table = [0, 0]

    select = False
    selected_position = []

    table = board.board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for x in range(board_height):
            for y in range(board_width):
                jewel.fill(table[x][y].colour())
                screen.blit(jewel, (x*50, y*50))

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

        if keys[pygame.K_SPACE]:
            print('space')
            print(selected_position)
            print(cursor_position_in_table)
            if select is False:
                select = True
                selected_position = tuple(cursor_position_in_table)
                print(selected_position)
            elif selected_position != cursor_position_in_table:
                print('x')
                select = False
                board.swap_jewels(selected_position, cursor_position_in_table)

        pygame.display.update()
        clock.tick(30)
