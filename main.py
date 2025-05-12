import pygame
import math
import random
from sys import exit
from enum import Enum

#setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Horse Race')
clock = pygame.time.Clock()
running = True
arena_background_image = pygame.image.load('graphics/arena.png')
arena_mask_image = pygame.mask.from_surface(arena_background_image)
game_speed = 2

class GameState(Enum):
    MENU = 0
    RACING = 1
    VICTORY = 2

game_state = GameState.MENU

class Horse:
    def __init__(self, name, sprite, x, y, scale, direction):
        self.name = name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.scale = scale
        self.direction = direction
        self.mask = pygame.mask.from_surface(sprite)

    def draw(self, screen):
        dir = self.direction % 360

        if dir < 90 or dir > 270: #facing right
            sprite = self.sprite
            screen.blit(sprite, (self.x, self.y))
        else: #facing left
            sprite = pygame.transform.flip(self.sprite, True, False)
            screen.blit(sprite, (self.x, self.y))

    def move(self, speed):
        r_dir = (self.direction * math.pi) / 180  # convert direction (degrees) to radian
        new_x = self.x + math.cos(r_dir) * speed
        new_y = self.y + math.sin(r_dir) * speed
        collision_range = 45

        #wall collision check
        if arena_mask_image.overlap(self.mask, (new_x-0, new_y-0)):
            self.direction += 180 + random.randrange(-collision_range, collision_range)
            return

        #other horses collision check
        for other in horses:
            if other == self:
                continue
            offset = ((other.x-new_x), (other.y-new_y))
            if self.mask.overlap(other.mask, offset):
                self.direction += 180 + random.randrange(-collision_range, collision_range)
                return

        #no collision
        self.x = new_x
        self.y = new_y


#spawn horses
horse_image = pygame.image.load('graphics/horse.png')
horse = Horse(name="Horse",sprite=horse_image,x=100,y=100,scale=1,direction=180)
horse_image = pygame.image.load('graphics/horse.png')
horse2 = Horse(name="Horse",sprite=horse_image,x=600,y=100,scale=1,direction=0)

horses = [horse, horse2]

#step
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #window close
            exit()

    #background
    screen.fill((0,0,0))
    screen.blit(arena_background_image, (0, 0))

    #horse
    horse.move(game_speed)
    horse2.move(game_speed)
    horse.draw(screen)
    horse2.draw(screen)


    pygame.display.update()
    clock.tick(60)

#end
pygame.quit()
