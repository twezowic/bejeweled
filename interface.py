from random import choice
import pygame
from sys import exit
from config import board_height, board_width, colors_of_jewels, number_of_jewels #  usunac number_of_jewels


def interface():
    pygame.init()
    screen = pygame.display.set_mode((board_width*50+210, board_height*50+10))
    block = pygame.Surface((50, 50))
    for i in range(number_of_jewels):
        block.fill(colors_of_jewels[i])
        screen.blit(block, (i*50,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


if __name__ == '__main__':
    interface()