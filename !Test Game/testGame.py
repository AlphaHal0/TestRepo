import pygame

from settings import *
from classes import *
from functions import *

FPS = 60

# Set fundamentals
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

font = pygame.font.Font(None, 256)

player = Player(1000, 1000, 20, 20, screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    core_functions(screen, clock, FPS)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]:
        player.move("down")
    if keys[pygame.K_UP]:
        player.move("up")
    
    player.display()
    
    pygame.display.update()

pygame.quit()