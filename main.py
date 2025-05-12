import sys
import glob
import pygame
import math
import random
from sys import exit
from enum import Enum

#setup
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('horseracetest')
clock = pygame.time.Clock()
running = True
arena_background_image = pygame.image.load('graphics/arena.png')
arena_mask_image = pygame.mask.from_surface(pygame.image.load('graphics/arena_mask.png'))

game_speed = 100

class GameState(Enum):
    MENU = 0
    RACING = 1
    VICTORY = 2

game_state = GameState.MENU
winner = None

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

class Reward:
    def __init__(self, sprite, x, y, scale):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.scale = scale
        self.mask = pygame.mask.from_surface(sprite)

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def rewardCheck(self):
        #other horses collision check
        for other in horses:
            offset = ((other.x-self.x), (other.y-self.y))
            if self.mask.overlap(other.mask, offset):
                global game_state
                global winner
                winner = other.name

                game_state = GameState.VICTORY
                print('winner is ' + str(winner))
                return


#spawn horses
horse_image = pygame.image.load('graphics/horse.png')
horse = Horse(name="GOREPLUSH VELLUMGRAVE",sprite=horse_image,x=100,y=100,scale=1,direction=180)
horse_image = pygame.image.load('graphics/horse2.png')
horse2 = Horse(name="WHITE [censored]",sprite=horse_image,x=600,y=100,scale=1,direction=0)
#horse count
horses = [horse, horse2]

#victory screen
victory_image = pygame.image.load('graphics/victory.png')

#spawn reward
reward_image = pygame.image.load('graphics/reward.png')
reward = Reward(sprite=reward_image,x=1070,y=70,scale=1)


#step
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #window close
            exit()

    #background
    screen.fill((0,0,0))
    screen.blit(arena_background_image, (0, 0))

    if game_state == GameState.MENU:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = GameState.RACING
                    game_time = 0
                    victory_animation = 0

        pass

    if game_state == GameState.RACING:
        #horse
        horse.move(game_speed)
        horse2.move(game_speed)
        reward.rewardCheck()
        if game_time == 0:
            pygame.mixer.init()
            track_list = glob.glob('tracklist/*.mp3')
            track = random.choice(track_list)
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play()
        game_time+=1


    #draw
    horse.draw(screen)
    horse2.draw(screen)

    reward.draw(screen)

    if game_state == GameState.VICTORY:
        if victory_animation == 0:
            pygame.mixer.init()
            track_list = glob.glob('sounds/victory*.mp3')
            track = random.choice(track_list)
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(.2)
            pygame.mixer.music.play()


        image_scale = victory_animation/100
        if image_scale > 1: image_scale = 1

        image = pygame.transform.scale_by(victory_image, image_scale)
        screen.blit(image, (screen_width/2-image.get_width()/2, screen_height/2-image.get_height()/2))

        def draw_winner_text (text, font, scale, max_width):
            #split long names
            words = text.split()
            lines = []
            current_line = ''

            #split text into multiple lines within max_width
            for word in words:
                test_line = current_line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + ' '
            if current_line:
                lines.append(current_line)

            #render each line
            rendered_lines = [font.render(line.strip(),True,(255,255,255)) for line in lines]
            line_height = font.get_linesize()*scale
            total_height = line_height * len(rendered_lines)

            #vertical center starting point
            y_offset = screen_height - total_height/2

            #render everything
            for i, line_surface in enumerate(rendered_lines):
                scaled_surface = pygame.transform.scale_by(line_surface,scale)
                x=screen_width/2 - scaled_surface.get_width()/2
                y=(y_offset+i*line_height - total_height/2) - 20
                screen.blit(scaled_surface, (x, y))

        draw_winner_text(
            text=winner,
            font=pygame.font.SysFont('Arial',24*4),
            scale=image_scale,
            max_width=screen_width-100
        )

        victory_animation += 1



        pass

    pygame.display.update()
    clock.tick(60)

#end
pygame.quit()
