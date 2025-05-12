import pygame
from sys import exit

#setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Horse Race')
clock = pygame.time.Clock()
running = True
arena_background = pygame.image.load('arena.png')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #window close
            exit()

    #fill the screen with this
    screen.blit(arena_background, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
