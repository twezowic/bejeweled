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
    position = [25, 25]
    table = board.board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for i in range(board_height):
            for j in range(board_width):
                jewel.fill(table[j][i])
                screen.blit(jewel, (j*50, i*50))

        keys = pygame.key.get_pressed()
        if position[0] != board_width * 50 - 25:
            position[0] += keys[pygame.K_RIGHT] * 50
        if position[0] != 25:
            position[0] -= keys[pygame.K_LEFT] * 50
        if position[1] != board_height * 50 - 25:
            position[1] += keys[pygame.K_DOWN] * 50
        if position[1] != 25:
            position[1] -= keys[pygame.K_UP] * 50
        screen.blit(cursor, (position))

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    interface()
